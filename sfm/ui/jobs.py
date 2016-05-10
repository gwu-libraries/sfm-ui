import json
from .rabbit import RabbitWorker
from .models import SeedSet, Harvest, default_uuid
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.conf import settings
from django.db import transaction

log = logging.getLogger(__name__)


@transaction.atomic
def seedset_harvest(seedset_pk):

    message = {
        "collection": {},
    }

    # Retrieve seedset
    try:
        seed_set = SeedSet.objects.get(id=seedset_pk)
    except ObjectDoesNotExist:
        log.error("Harvesting seedset %s failed because seedset does not exist", seedset_pk)
        return

    if not seed_set.is_active:
        log.debug("Ignoring Harvest for seedset as seedset %s is inactive", seedset_pk)
        return

    historical_seed_set = seed_set.history.all()[0]
    historical_credential = historical_seed_set.credential.history.all()[0]
    historical_seeds = []
    for seed in seed_set.seeds.all():
        if seed.is_active:
            historical_seeds.append(seed.history.all()[0])
        else:
            log.debug("Seed %s is ignored from the harvest as it is inactive", seed)

    # Make sure that have the correct number of seeds.
    required_seed_count = seed_set.required_seed_count()
    if (required_seed_count is None and len(historical_seeds) == 0) or (
            required_seed_count is not None and required_seed_count != len(historical_seeds)):
        log.warning("Seedset %s has wrong number of active seeds.", seedset_pk)
        return

    # Id
    harvest_id = default_uuid()
    message["id"] = harvest_id

    # Collection
    collection = historical_seed_set.collection
    message["collection"]["id"] = collection.collection_id
    message["path"] = "{}/collection/{}/{}".format(settings.SFM_DATA_DIR, collection.collection_id, seed_set.seedset_id)

    # Credential
    message["credentials"] = json.loads(str(historical_credential.token))

    # Type
    harvest_type = historical_seed_set.harvest_type
    message["type"] = harvest_type

    # Options
    message["options"] = json.loads(historical_seed_set.harvest_options or "{}")

    # Seeds
    if historical_seeds:
        message["seeds"] = []
        for historical_seed in historical_seeds:
            if historical_seed.is_active:
                seed_map = dict()
                seed_map["id"] = historical_seed.seed_id
                if historical_seed.token:
                    seed_map["token"] = historical_seed.token
                if historical_seed.uid:
                    seed_map["uid"] = historical_seed.uid
                message["seeds"].append(seed_map)

    routing_key = "harvest.start.{}.{}".format(historical_credential.platform,
                                               harvest_type)

    log.debug("Sending %s message to %s with id %s", harvest_type,
              routing_key, harvest_id)

    # Publish message to queue via rabbit worker
    RabbitWorker().send_message(message, routing_key)

    # Record harvest model instance
    harvest = Harvest.objects.create(harvest_type=harvest_type,
                                     harvest_id=harvest_id,
                                     seed_set=seed_set,
                                     historical_seed_set=historical_seed_set,
                                     historical_credential=historical_credential)
    harvest.historical_seeds.add(*historical_seeds)


@transaction.atomic
def seedset_stop(seedset_id):

    # Retrieve seedset
    try:
        seed_set = SeedSet.objects.get(id=seedset_id)
    except ObjectDoesNotExist:
        log.error("Stopping harvest of %s failed because seedset does not exist", seedset_id)
        return
    harvest = seed_set.last_harvest()
    assert seed_set.is_streaming()
    if harvest is None or harvest.status not in (Harvest.REQUESTED, Harvest.RUNNING):
        log.debug("Ignoring stop harvest of seedset since %s does not have a running harvest.")
        return

    message = {
        "id": harvest.harvest_id
    }

    routing_key = "harvest.stop.{}.{}".format(harvest.historical_credential.platform, harvest.harvest_type)

    log.debug("Sending %s stop message to %s with id %s", harvest.harvest_type, routing_key, harvest.harvest_id)

    # Publish message to queue via rabbit worker
    RabbitWorker().send_message(message, routing_key)

    # Update harvest model instance
    harvest.status = Harvest.STOP_REQUESTED
    harvest.save()