import json
from .rabbit import RabbitWorker
from .models import SeedSet, Harvest
from django.core.exceptions import ObjectDoesNotExist
import logging
import datetime
from django.conf import settings

log = logging.getLogger(__name__)


def seedset_harvest(seedset_id):

    message = {
        "collection": {},
        "seeds": []
    }

    # Retrieve seedset
    try:
        seedset = SeedSet.objects.get(id=seedset_id)
    except ObjectDoesNotExist:
        log.error("Harvesting seedset %s failed because seedset does not exist", seedset_id)
        return

    # Id
    harvest_id = "harvest:{}:{}".format(seedset_id, datetime.datetime.now().isoformat())
    message["id"] = harvest_id

    # Collection
    collection = seedset.collection
    message["collection"]["id"] = "collection:{}".format(collection.id)
    message["collection"]["path"] = "{}/collection/{}".format(settings.SFM_DATA_DIR, collection.id)

    # Credential
    credentials = seedset.credential
    message["credentials"] = json.loads(str(credentials.token))

    # Type
    harvest_type = seedset.harvest_type
    message["type"] = harvest_type

    # Options
    message["options"] = json.loads(seedset.harvest_options or "{}")

    # Seeds
    seeds = seedset.seeds.all()
    if not seeds:
        log.warning("Seedset %s has no seeds", seedset_id)
        return

    for seed in seeds:

        seed_map = {}
        if seed.is_active:
            if seed.token:
                seed_map["token"] = seed.token
            if seed.uid:
                seed_map["uid"] = seed.uid
            message["seeds"].append(seed_map)
        else:
            log.debug("Seed %s is ignored from the harvest as it is inactive",
                      seed)


    # Include conditions to check Is Active Flag here.
    # We can include a simple if condition here to check active collections.
    if seedset.is_active:

        routing_key = "harvest.start.{}.{}".format(credentials.platform, harvest_type)

        log.debug("Sending %s message to %s with id %s", harvest_type, routing_key, harvest_id)

        # Publish message to queue via rabbit worker
        RabbitWorker().send_message(message, routing_key)

        # Record harvest model instance
        Harvest.objects.create(seed_set=seedset,
                       harvest_id=harvest_id)
    else:
        log.debug("Ignoring Harvest for seedset as seedset %s is inactive",
                  seedset_id)
