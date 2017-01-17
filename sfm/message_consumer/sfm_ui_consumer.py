import logging
from sfmutils.consumer import BaseConsumer
from sfmutils.harvester import CODE_UNKNOWN_ERROR
from ui.models import User, Harvest, Collection, Seed, Warc, Export, HarvestStat
from ui.jobs import collection_stop
from ui.utils import get_email_addresses_for_collection_set
from ui.export import create_readme_for_export

import json
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
import iso8601
import time
from smtplib import SMTPException
import os
import codecs

log = logging.getLogger(__name__)


class SfmUiConsumer(BaseConsumer):
    """
    Class for the SFM UI Consumer, which subscribes to
    messages from the queue and updates the models as appropriate.
    """

    def on_message(self):
        # This is the worst ever, but it avoids a race condition.
        # It is possible for the harvester/exporter to respond before the commit occurs.
        time.sleep(1)

        if self.routing_key.startswith("harvest.status."):
            self._on_harvest_status_message()
        elif self.routing_key == "warc_created":
            self._on_warc_created_message()
        elif self.routing_key.startswith("export.status."):
            self._on_export_status_message()
        elif self.routing_key == "harvest.start.web":
            self._on_web_harvest_start_message()
        else:
            log.warn("Unexpected message with routing key %s: %s", self.routing_key, json.dumps(self.message, indent=4))

    def _on_harvest_status_message(self):
        try:
            log.debug("Updating harvest with id %s", self.message["id"])
            # Retrieve harvest model object
            harvest = Harvest.objects.get(harvest_id=self.message["id"])

        except ObjectDoesNotExist:
            log.error("Harvest model object not found for harvest status message: %s",
                      json.dumps(self.message, indent=4))
            return

        # And update harvest model object
        harvest.status = self.message["status"]
        harvest.infos = self.message.get("infos", [])
        harvest.warnings = self.message.get("warnings", [])
        harvest.errors = self.message.get("errors", [])
        harvest.token_updates = self.message.get("token_updates")
        harvest.uids = self.message.get("uids")
        harvest.warcs_count = self.message.get("warcs", {}).get("count", 0)
        harvest.warcs_bytes = self.message.get("warcs", {}).get("bytes", 0)
        harvest.date_started = iso8601.parse_date(self.message["date_started"])
        if "date_ended" in self.message:
            harvest.date_ended = iso8601.parse_date(self.message["date_ended"])
        harvest.service = self.message.get("service")
        harvest.host = self.message.get("host")
        harvest.instance = self.message.get("instance")
        harvest.save()

        # Update seeds based on tokens that have changed
        for seed_id, token in self.message.get("token_updates", {}).items():
            # Handle case when token comes back None
            if token:
                # Try to find seed based on collection and uid.
                try:
                    seed = Seed.objects.get(seed_id=seed_id)
                    seed.token = token
                    seed.history_note = "Changed token based on information from harvester from harvest {}".format(
                        self.message["id"])
                    seed.save()
                except ObjectDoesNotExist:
                    log.error("Seed model object with seed_id %s not found to update token to %s", seed_id, token)

        # Update seeds based on uids that have been returned
        for seed_id, uid in self.message.get("uids", {}).items():
            # Try to find seed based on collection and token.
            try:
                seed = Seed.objects.get(seed_id=seed_id)
                seed.uid = uid
                seed.history_note = "Changed uid based on information from harvester from harvest {}".format(
                    self.message["id"])
                seed.save()
            except ObjectDoesNotExist:
                log.error("Seed model object with seed_id %s not found to update uid to %s", seed_id, uid)

        # Update stats
        if self.message["status"] != Harvest.FAILURE:
            day_stats = self.message.get("stats", {})

            for day_str, stat in day_stats.items():
                day = iso8601.parse_date(day_str).date()
                for item, count in stat.items():
                    try:
                        stat = harvest.harvest_stats.get(item=item, harvest_date=day)
                        stat.count = count
                        stat.save()
                    except ObjectDoesNotExist:
                        HarvestStat.objects.create(item=item, harvest=harvest, count=count, harvest_date=day)

        # Turn off stream collections if they failed
        turned_collection_off = False
        if harvest.status == Harvest.FAILURE and harvest.collection.is_streaming():
            log.info("Turning collection %s off", harvest.collection.name)
            harvest.collection.is_active = False
            harvest.collection.history_note = "Turning off due to a failed harvest ({})".format(self.message["id"])
            harvest.collection.save()
            # Send stop message
            collection_stop(harvest.collection.id)
            turned_collection_off = True

        # Send email if completed and failed or has messages
        if harvest.status == Harvest.FAILURE or (
                        harvest.status in (Harvest.SUCCESS, Harvest.PAUSED) and (
                            harvest.infos or harvest.warnings or harvest.errors)):

            # Get emails for group members
            receiver_emails = get_email_addresses_for_collection_set(harvest.collection.collection_set,
                                                                     use_harvest_notification_preference=True,
                                                                     include_admins=False)

            # Check if harvest errors contains UNKNOWN_ERRORS
            for msg in harvest.errors:
                if msg['code'] == CODE_UNKNOWN_ERROR:
                    log.debug("Harvest has unknown error so also sending to admins")
                    for user in User.objects.filter(is_superuser=True):
                        if user.email and user.harvest_notifications:
                            receiver_emails.append(user.email)
                    break

            if receiver_emails:
                harvest_url = 'http://{}{}'.format(Site.objects.get_current().domain,
                                                   reverse('harvest_detail', args=(harvest.id,)))

                # Send Status mail
                if settings.PERFORM_EMAILS:
                    if harvest.status == Harvest.SUCCESS:
                        mail_subject = u"SFM Harvest for {} completed successfully, but has messages".format(
                            harvest.collection.name)
                        mail_message = u"The harvest for {} ({}) completed successfully, but has messages.".format(
                            harvest.collection.name,
                            harvest_url)
                    # Failure
                    else:
                        mail_subject = u"SFM Harvest for {} failed".format(harvest.collection.name)
                        mail_message = u"The harvest for {} ({}) failed.".format(harvest.collection.name,
                                                                                 harvest_url)
                    if turned_collection_off:
                        mail_message += "\n\nThis collection has been turned off."
                    mail_message += self.format_messages_for_mail(harvest.infos, "informational")
                    mail_message += self.format_messages_for_mail(harvest.warnings, "warning")
                    mail_message += self.format_messages_for_mail(harvest.errors, "error")

                    try:
                        log.debug("Sending email to %s: %s", receiver_emails, mail_subject)
                        send_mail(mail_subject, mail_message, settings.EMAIL_HOST_USER,
                                  receiver_emails, fail_silently=False)
                    except SMTPException, ex:
                        log.error("Error sending email: %s", ex)
                    except IOError, ex:
                        log.error("Error sending email: %s", ex)
            else:
                log.warn("No email addresses for %s", harvest.collection.collection_set.group)

    @staticmethod
    def format_messages_for_mail(messages, message_type):
        mail_message = ""
        if messages:
            mail_message += "\n\n{} messages:\n".format(message_type.title())
            for msg in messages:
                mail_message += "- {}\n".format(msg["message"])
        return mail_message

    def _on_warc_created_message(self):
        try:
            log.debug("Warc with id %s", self.message["warc"]["id"])
            # Create warc model object
            warc = Warc.objects.create(
                harvest=Harvest.objects.get(harvest_id=self.message["harvest"]["id"]),
                warc_id=self.message["warc"]["id"],
                path=self.message["warc"]["path"],
                sha1=self.message["warc"]["sha1"],
                bytes=self.message["warc"]["bytes"],
                date_created=iso8601.parse_date(self.message["warc"]["date_created"])
            )
            warc.save()

        except ObjectDoesNotExist:
            log.error("Harvest model object not found for harvest status message: %s",
                      json.dumps(self.message, indent=4))

    def _on_export_status_message(self):
        try:
            log.debug("Updating export with id %s", self.message["id"])
            # Retrieve export model object
            export = Export.objects.get(export_id=self.message["id"])
            # And update export model object
            export.status = self.message["status"]
            export.infos = self.message.get("infos", [])
            export.warnings = self.message.get("warnings", [])
            export.errors = self.message.get("errors", [])
            export.date_started = iso8601.parse_date(self.message["date_started"])
            if "date_ended" in self.message:
                export.date_ended = iso8601.parse_date(self.message["date_ended"])
            export.service = self.message.get("service")
            export.host = self.message.get("host")
            export.instance = self.message.get("instance")
            export.save()

            # Write README
            if os.path.exists(export.path):
                readme_txt = create_readme_for_export(export)
                readme_filepath = os.path.join(export.path, "README.txt")
                log.debug("Writing export README to %s: %s", readme_filepath, readme_txt)
                with codecs.open(readme_filepath, "w", encoding="utf-8") as f:
                    f.write(readme_txt)

            else:
                log.warn("Not writing export README for %s since %s does not exist.", export, export.path)

            if export.status in (Export.SUCCESS, Export.FAILURE):
                # Get receiver's email address
                receiver_email = export.user.email
                if receiver_email:
                    export_url = 'http://{}{}'.format(Site.objects.get_current().domain,
                                                      reverse('export_detail', args=(export.id,)))

                    # Send Status mail
                    if settings.PERFORM_EMAILS:
                        collection = export.collection if export.collection else export.seeds.first().collection
                        mail_message = None
                        mail_subject = None
                        if export.status == 'completed success':
                            mail_message = u"Your export of {} is ready. You can retrieve it from {}.".format(
                                collection.name,
                                export_url)
                            mail_subject = "SFM Export is ready"
                        elif export.status == 'completed failure':
                            mail_message = u"Your export of {} failed. You can get more information from {}".format(
                                collection.name, export_url)
                            mail_subject = "SFM Export failed"
                        else:
                            log.debug("Unhandled export status: %s", export.status)
                        if mail_message:
                            try:
                                log.debug("Sending email to %s: %s", receiver_email, mail_subject)
                                send_mail(mail_subject, mail_message, settings.EMAIL_HOST_USER,
                                          [receiver_email], fail_silently=False)
                            except SMTPException, ex:
                                log.error("Error sending email: %s", ex)
                            except IOError, ex:
                                log.error("Error sending email: %s", ex)

                else:
                    log.warn("No email address for %s", export.user)

        except ObjectDoesNotExist:
            log.error("Export model object not found for export status message: %s",
                      json.dumps(self.message, indent=4))

    def _on_web_harvest_start_message(self):
        try:
            log.debug("Creating harvest for web harvest with id %s", self.message["id"])
            parent_harvest = Harvest.objects.get(harvest_id=self.message["parent_id"])
            harvest = Harvest.objects.create(harvest_type=self.message["type"],
                                             harvest_id=self.message["id"],
                                             parent_harvest=parent_harvest,
                                             collection=parent_harvest.collection)
            harvest.save()
        except ObjectDoesNotExist:
            log.error("Harvest model object not found for web harvest status message: %s",
                      json.dumps(self.message, indent=4))
