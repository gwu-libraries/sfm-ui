import logging
from sfmutils.consumer import BaseConsumer
from ui.models import Harvest, SeedSet, Seed
import json
from django.core.exceptions import ObjectDoesNotExist
import iso8601

log = logging.getLogger(__name__)


class SfmUiConsumer(BaseConsumer):
    """
    Class for the SFM UI Consumer, which subscribes to
    messages from the queue and updates the models as appropriate.
    """
    def on_message(self):
        if self.routing_key.startswith("harvest.status."):
            try:
                log.debug("Updating harvest with id {}", self.message["id"])
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
                for uid, token in self.message.get("token_updates", {}).items():
                    # Try to find seed based on seedset and uid.
                    try:
                        seed = Seed.objects.get(seed_set=harvest.seed_set, uid=uid)
                        seed.token = token
                        seed.note = "Updated token based on harvest {}".format(self.message["id"])
                        seed.save()
                    except ObjectDoesNotExist:
                        log.error("Seed model object with uid {} not found to update token to {}", uid, token)

                # Update seeds based on uids that have been returned
                for token, uid in self.message.get("uids", {}).items():
                    # Try to find seed based on seedset and token.
                    try:
                        seed = Seed.objects.get(seed_set=harvest.seed_set, token=token)
                        seed.uid = uid
                        seed.note = "Updated uid based on harvest {}".format(self.message["id"])
                        seed.save()
                    except ObjectDoesNotExist:
                        log.error("Seed model object with token {} not found to update uid to {}", token, uid)

            except ObjectDoesNotExist:
                log.error("Harvest model object not found for harvest status message: {}",
                          json.dumps(self.message, indent=4))
        else:
            log.warn("Unexpected message with routing key {}: {}", self.routing_key, json.dumps(self.message, indent=4))
