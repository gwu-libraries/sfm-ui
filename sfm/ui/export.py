import logging

from django.utils import timezone
from django.template.loader import get_template

from .models import Export
from .utils import diff_collection_and_seeds_history
from .rabbit import RabbitWorker
from sfmutils.utils import datetime_now

log = logging.getLogger(__name__)


def export_receiver(sender, **kwargs):
    assert kwargs["instance"]

    log.debug("Export receiver invoked")

    if kwargs.get("created", False):
        request_export(kwargs["instance"])


def export_m2m_receiver(sender, **kwargs):
    assert kwargs["instance"]
    assert kwargs["action"]

    log.debug("Export m2m receiver invoked with action %s", kwargs["action"])

    if kwargs["action"] == "post_add":
        request_export(kwargs["instance"])


def request_export(export):
    # Return if already requested
    if export.status != Export.NOT_REQUESTED:
        log.debug("Export %s already requested", export.export_id)
        return

    # Return if no seeds or collections. Many-to-many like seeds are added after save.
    # Will wait for m2m_changed to request export.
    if not export.collection and not export.seeds.all():
        log.debug("No seeds or collections yet")
        return

    message = {
        "id": export.export_id,
        "type": export.export_type,
        "format": export.export_format,
        "segment_size": export.export_segment_size,
        "dedupe": export.dedupe,
        "path": export.path
    }

    platform = None
    if export.collection:
        message["collection"] = {"id": export.collection.collection_id}
        platform = export.collection.credential.platform

    seeds = []
    for seed in export.seeds.all():
        seeds.append({"id": seed.seed_id, "uid": seed.uid})
        platform = seed.collection.credential.platform
    if seeds:
        message["seeds"] = seeds

    if export.item_date_start:
        message["item_date_start"] = export.item_date_start.isoformat()
    if export.item_date_end:
        message["item_date_end"] = export.item_date_end.isoformat()
    if export.harvest_date_start:
        message["harvest_date_start"] = export.harvest_date_start.isoformat()
    if export.harvest_date_end:
        message["harvest_date_end"] = export.harvest_date_end.isoformat()

    routing_key = "export.start.{}.{}".format(platform, export.export_type)

    log.debug("Sending %s message to %s with id %s", export.export_type, routing_key, export.export_id)

    # Publish message to queue via rabbit worker
    RabbitWorker().send_message(message, routing_key)

    # Update date requested
    export.date_requested = timezone.now()
    export.status = Export.REQUESTED
    export.save()


def _create_readme(collection, export, now):
    readme_template = get_template('readme/export.txt')
    return readme_template.render({"collection": collection,
                                   "export": export,
                                   "diffs": diff_collection_and_seeds_history(collection),
                                   "now": now})


def create_readme_for_collection(collection):
    return _create_readme(collection, None, datetime_now())


def create_readme_for_export(export):
    # An export will have seeds or collection
    return _create_readme(export.collection if export.collection else export.seeds.all()[0].collection, export,
                          export.date_ended)
