from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from django.conf import settings
import logging
from .jobs import collection_harvest, collection_stop
from .models import Collection, Harvest
import datetime
from .utils import diff_field_changed
from django.core.exceptions import ObjectDoesNotExist

log = logging.getLogger(__name__)

sched = BackgroundScheduler()


def start_sched():
    sched.configure(jobstores={
        'default': SQLAlchemyJobStore(url=settings.SCHEDULER_DB_URL)
    })
    log.info("Starting scheduler")
    sched.start()
    return sched


def next_run_time(collection_pk):
    job_id = _job_id(collection_pk)
    job = sched.get_job(job_id)
    if job and hasattr(job, 'next_run_time'):
        return job.next_run_time
    else:
        return None


def _job_id(collection_pk):
    return str(collection_pk)


def _end_job_id(collection_pk):
    return "end_{}".format(collection_pk)


def unschedule_harvest(collection_pk):
    _unschedule_job(_job_id(collection_pk))
    _unschedule_job(_end_job_id(collection_pk))


def _unschedule_job(job_id):
    if sched.get_job(job_id) is not None:
        log.debug("Unscheduling job %s", job_id)
        sched.remove_job(job_id)


def toggle_collection_inactive(collection_id):
    try:
        collection = Collection.objects.get(id=collection_id)
    except ObjectDoesNotExist:
        log.error("Toggling collection %s to inactive failed because collection does not exist", collection_id)
        return
    log.debug("Toggling collection %s to inactive and clearing end date.", collection_id)
    collection.is_on = False
    collection.end_date = None
    collection.history_note = "Turning off since reached end date or one-time harvest."
    collection.save()


def schedule_harvest(collection_pk, is_on, schedule_minutes, start_date=None, end_date=None):
    assert schedule_minutes

    unschedule_harvest(collection_pk)
    log.debug("Collection %s is on = %s", collection_pk, is_on)
    if is_on:
        name = "Harvest ({}) for collection {}".format(schedule_minutes, collection_pk)
        log.debug("Scheduling job %s", name)
        sched.add_job(collection_harvest,
                      args=[collection_pk],
                      id=_job_id(collection_pk),
                      name=name,
                      trigger='interval',
                      start_date=start_date,
                      end_date=end_date,
                      minutes=schedule_minutes)

        if schedule_minutes == 1:
            end_date = start_date

        if end_date:
            log.debug("Scheduling end job for %s to run at %s", name, end_date)
            sched.add_job(toggle_collection_inactive,
                          args=[collection_pk],
                          id=_end_job_id(collection_pk),
                          name="End harvest for collection {}".format(collection_pk),
                          trigger='date',
                          run_date=end_date)


def schedule_stream_harvest(collection_pk, is_on, start_date=None, end_date=None, last_harvest_status=None):
    unschedule_harvest(collection_pk)

    log.debug("Collection %s is active = %s", collection_pk, is_on)
    if is_on:
        name = "Harvest for collection {}".format(collection_pk)
        log.debug("Scheduling job %s", name)
        sched.add_job(collection_harvest,
                      args=[collection_pk],
                      id=_job_id(collection_pk),
                      name=name,
                      trigger='date',
                      run_date=start_date)

        if end_date:
            log.debug("Scheduling end job for %s to run at %s", name, end_date)
            sched.add_job(toggle_collection_inactive,
                          args=[collection_pk],
                          id=_end_job_id(collection_pk),
                          name="End harvest for collection {}".format(collection_pk),
                          trigger='date',
                          run_date=end_date)
    # If not active and last harvest requested or running
    elif last_harvest_status in (Harvest.REQUESTED, Harvest.RUNNING):
        log.debug("Stopping collection %s", collection_pk)
        collection_stop(collection_pk)


def schedule_harvest_receiver(sender, **kwargs):
    assert kwargs["instance"]
    collection = kwargs["instance"]

    if diff_field_changed(collection):
        if collection.is_streaming():
            last_harvest = collection.last_harvest()
            schedule_stream_harvest(collection.id, collection.is_on,
                                    start_date=datetime.datetime.now() + datetime.timedelta(seconds=15),
                                    end_date=collection.end_date or None,
                                    last_harvest_status=last_harvest.status if last_harvest else None)
        else:
            schedule_harvest(collection.id, collection.is_on, collection.schedule_minutes,
                             start_date=datetime.datetime.now() + datetime.timedelta(seconds=15),
                             end_date=collection.end_date or None)
    else:
        log.debug("Skipping scheduling harvest of collection %s since nothing significant changed.", collection.pk)


def unschedule_harvest_receiver(sender, **kwargs):
    assert kwargs["instance"]
    collection = kwargs["instance"]

    unschedule_harvest(collection.id)
