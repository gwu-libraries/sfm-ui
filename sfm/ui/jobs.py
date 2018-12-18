import json
import logging
from smtplib import SMTPException

from .rabbit import RabbitWorker
from .models import Collection, Harvest, default_uuid
from .utils import collection_path, get_email_addresses_for_collection_set

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.urls import reverse
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings

log = logging.getLogger(__name__)


def collection_harvest(collection_pk):
    with transaction.atomic():
        message = {
            "collection_set": {},
            "collection": {}
        }

        # Retrieve collection
        try:
            collection = Collection.objects.get(id=collection_pk)
        except ObjectDoesNotExist:
            log.error("Harvesting collection %s failed because collection does not exist", collection_pk)
            return

        if not collection.is_on:
            log.debug("Ignoring Harvest for collection as collection %s is off", collection_pk)
            return

        historical_collection = collection.history.all()[0]
        historical_credential = historical_collection.credential.history.all()[0]
        historical_seeds = []
        for seed in collection.seeds.all():
            if seed.is_active:
                historical_seeds.append(seed.history.all()[0])
            else:
                log.debug("Seed %s is ignored from the harvest as it is inactive", seed)

        # Make sure that have the correct number of seeds.
        required_seed_count = collection.required_seed_count()
        if (required_seed_count is None and len(historical_seeds) == 0) or (
                required_seed_count is not None and required_seed_count != len(historical_seeds)):
            log.warning("Collection %s has wrong number of active seeds.", collection_pk)
            return

        # Id
        harvest_id = default_uuid()
        message["id"] = harvest_id

        # Collection set
        collection_set = historical_collection.collection_set
        message["collection_set"]["id"] = collection_set.collection_set_id

        # Collection
        message["collection"]["id"] = historical_collection.collection_id

        # Path
        message["path"] = collection_path(collection)

        # Credential
        message["credentials"] = json.loads(str(historical_credential.token))

        # Type
        harvest_type = historical_collection.harvest_type
        message["type"] = harvest_type

        # Options
        message["options"] = json.loads(historical_collection.harvest_options or "{}")

        # Seeds
        if historical_seeds:
            message["seeds"] = []
            for historical_seed in historical_seeds:
                if historical_seed.is_active:
                    seed_map = dict()
                    seed_map["id"] = historical_seed.seed_id
                    if historical_seed.token:
                        # This may be json
                        try:
                            seed_map["token"] = json.loads(historical_seed.token)
                        except ValueError:
                            seed_map["token"] = historical_seed.token
                    if historical_seed.uid:
                        seed_map["uid"] = historical_seed.uid
                    message["seeds"].append(seed_map)

        routing_key = "harvest.start.{}.{}".format(historical_credential.platform,
                                                   harvest_type)
        # Determine if .priority should be appended
        if collection.harvest_type in settings.PRIORITY_HARVEST_TYPES \
                and collection.schedule_minutes \
                and collection.schedule_minutes <= settings.PRIORITY_SCHEDULE_MINUTES:
            routing_key += ".priority"

        # Skip this harvest if last harvest not completed or voided
        last_harvest = collection.last_harvest()
        if not last_harvest or last_harvest.status in (Harvest.SUCCESS, Harvest.FAILURE, Harvest.VOIDED):
            # Record harvest model instance
            harvest = Harvest.objects.create(harvest_type=harvest_type,
                                             harvest_id=harvest_id,
                                             collection=collection,
                                             historical_collection=historical_collection,
                                             historical_credential=historical_credential)
            harvest.historical_seeds.add(*historical_seeds)
        else:
            log.warning("Skipping harvest with id %s", harvest_id)

            # Set message to None to indicate that should not be sent
            message = None

            # Record harvest model instance
            harvest = Harvest.objects.create(harvest_type=harvest_type,
                                             harvest_id=harvest_id,
                                             collection=collection,
                                             historical_collection=historical_collection,
                                             historical_credential=historical_credential,
                                             status=Harvest.SKIPPED)
            harvest.historical_seeds.add(*historical_seeds)

            # Send notifications
            if settings.PERFORM_EMAILS:
                receiver_emails = get_email_addresses_for_collection_set(harvest.collection.collection_set,
                                                                         use_harvest_notification_preference=True,
                                                                         include_admins=True)
                harvest_url = 'http://{}{}'.format(Site.objects.get_current().domain,
                                                   reverse('harvest_detail', args=(harvest.id,)))
                mail_subject = u"SFM Harvest for {} was skipped".format(
                    harvest.collection.name)
                mail_message = u"The harvest for {} ({}) was skipped. This may be because it is scheduled too " \
                               u"frequently and the last harvest has not had time to complete. It " \
                               u"may also indicate a problem with SFM. The SFM administrator has been notified.".format(
                                harvest.collection.name, harvest_url)

                if receiver_emails:
                    try:
                        log.debug("Sending email to %s: %s", receiver_emails, mail_subject)
                        send_mail(mail_subject, mail_message, settings.EMAIL_FROM,
                                  receiver_emails, fail_silently=False)
                    except SMTPException as ex:
                        log.error("Error sending email: %s", ex)
                    except IOError as ex:
                        log.error("Error sending email: %s", ex)

    # Send message outside the transaction
    if message:
        log.info("Sending %s message to %s with id %s for collection %s", harvest_type,
                 routing_key, harvest_id, collection_pk)

        # Publish message to queue via rabbit worker
        RabbitWorker().send_message(message, routing_key)


@transaction.atomic
def collection_stop(collection_id):
    # Retrieve collection
    try:
        collection = Collection.objects.get(id=collection_id)
    except ObjectDoesNotExist:
        log.error("Stopping harvest of %s failed because collection does not exist", collection_id)
        return
    harvest = collection.last_harvest()
    assert collection.is_streaming()
    if harvest is None or harvest.status not in (Harvest.REQUESTED, Harvest.RUNNING, Harvest.FAILURE):
        log.debug("Ignoring stop harvest of collection since %s does not have a running harvest.")
        return

    message = {
        "id": harvest.harvest_id
    }

    routing_key = "harvest.stop.{}.{}".format(harvest.historical_credential.platform, harvest.harvest_type)

    log.info("Sending %s stop message to %s with id %s for collection %s", harvest.harvest_type, routing_key,
             harvest.harvest_id, collection_id)

    # Publish message to queue via rabbit worker
    RabbitWorker().send_message(message, routing_key)

    # Update harvest model instance
    if harvest.status in (Harvest.REQUESTED, Harvest.RUNNING):
        harvest.status = Harvest.STOP_REQUESTED
        harvest.save()
