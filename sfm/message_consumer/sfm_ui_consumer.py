import logging
from sfmutils.consumer import BaseConsumer
from ui.models import Harvest, SeedSet, Seed, Warc, Export
import json
from django.core.exceptions import ObjectDoesNotExist
import iso8601
import time

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

            # And update harvest model object
            harvest.status = self.message["status"]
            harvest.stats = self.message.get("summary", {})
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
            harvest.save()

            # Update seeds based on tokens that have changed
            for id, token in self.message.get("token_updates", {}).items():
                # Try to find seed based on seedset and uid.
                try:
                    seed = Seed.objects.get(seed_id=id)
                    seed.token = token
                    seed.history_note = "Changed token based on information from harvester from harvest {}".format(
                            self.message["id"])
                    seed.save()
                except ObjectDoesNotExist:
                    log.error("Seed model object with seed_id %s not found to update token to %s", id, token)

            # Update seeds based on uids that have been returned
            for id, uid in self.message.get("uids", {}).items():
                # Try to find seed based on seedset and token.
                try:
                    seed = Seed.objects.get(seed_id=id)
                    seed.uid = uid
                    seed.history_note = "Changed uid based on information from harvester from harvest {}".format(
                            self.message["id"])
                    seed.save()
                except ObjectDoesNotExist:
                    log.error("Seed model object with seed_id %s not found to update uid to %s", id, uid)

        except ObjectDoesNotExist:
            log.error("Harvest model object not found for harvest status message: %s",
                      json.dumps(self.message, indent=4))

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
            export.save()

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
                                             seed_set=parent_harvest.seed_set)
            harvest.save()
        except ObjectDoesNotExist:
            log.error("Harvest model object not found for web harvest status message: %s",
                      json.dumps(self.message, indent=4))

        # {
        #     "id": "flickr:45",
        #     "parent_id": "sfmui:45",
        #     "type": "web",
        #     "seeds": [
        #         {
        #             "token": "http://www.gwu.edu/"
        #         },
        #         {
        #             "token": "http://library.gwu.edu/"
        #         }
        #     ],
        #     "collection": {
        #         "id": "test_collection",
        #         "path": "/tmp/test_collection"
        #     }
        # }
