import json
from .rabbit import RabbitWorker
from .models import SeedSet, Collection, Seed, Credential
import datetime
import logging
from sfmutils.consumer import EXCHANGE

log = logging.getLogger(__name__)

def seedset_harvest(d):
    # To get value of Collection id for the associated collection object.
    for collection_id in list(Collection.objects.filter(
        id=SeedSet.objects.filter(id=d).values('collection')).values('id')):
        if 'id' in collection_id:
            value=collection_id['id']

    # To get value of the token for the associated credential object.
    for token in list(Credential.objects.filter(
        id=SeedSet.objects.filter(id=d).values('credential')).values(
            'token')):
        if 'token' in token:
            credential = token['token']

    # To get value of platform
    for platform in list(Credential.objects.filter(
        id=SeedSet.objects.filter(id=d).values('credential')).values(
            'platform')):
        if 'platform' in platform:
            media = platform['platform']

    # To get list of seeds
    seeds = list(Seed.objects.filter(seed_set=d).select_related(
        'seeds').values('token', 'uid'))
    # To remove empty token values from the list of seeds --
    # Need to update below code
    #
    # if item['token'] not in seeds:
        # item.pop('token', None)
    for item in seeds:
        if item['token'] == '':
            item.pop('token', None)

    # To get harvest type, options and credentials
    harvest_type = SeedSet.objects.filter(id=d).values(
        'harvest_type')[0]["harvest_type"]
    options = json.loads(SeedSet.objects.filter(id=d).values(
        'harvest_options')[0]["harvest_options"])
    credential = json.loads(str(credential))

    # Routing Key
    key = ''.join(['harvest.start.',str(media),'.',harvest_type])

    # message to be sent to queue
    # TODO: Unique id
    # TODO: Correct path
    m = {
        'id': d,
        'type': harvest_type,
        'options': options,
        'credentials': credential,
        'collection': {
            'id': str(value),
            'path': '/tmp/collection/'+str(value)
        },
        'seeds': seeds,
    }

    log.info("Sending %s message to %s with id %s", harvest_type, key,
             m["id"])
    log.debug("Message with id %s is %s", m["id"], json.dumps(m, indent=4))

    # Publish message to queue via rabbit worker
    RabbitWorker.channel.basic_publish(exchange=EXCHANGE,
                                       routing_key=key,body=json.dumps(m))
