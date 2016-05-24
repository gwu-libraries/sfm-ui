from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from django.conf import settings
import logging
from jobs import seedset_harvest, seedset_stop
from models import SeedSet, Harvest
import datetime
from utils import diff_field_changed
from django.core.exceptions import ObjectDoesNotExist

log = logging.getLogger(__name__)

sched = BackgroundScheduler()


def start_sched():
    sched.configure(jobstores={
        'default': SQLAlchemyJobStore(url=settings.SCHEDULER_DB_URL)
    })
    log.info("Starting scheduler")
    sched.start()


def next_run_time(seedset_pk):
    job_id = _job_id(seedset_pk)
    job = sched.get_job(job_id)
    if job:
        return job.next_run_time
    else:
        return None


def _job_id(seedset_pk):
    return str(seedset_pk)


def _end_job_id(seedset_pk):
    return "end_{}".format(seedset_pk)


def unschedule_harvest(seedset_pk):
    _unschedule_job(_job_id(seedset_pk))
    _unschedule_job(_end_job_id(seedset_pk))


def _unschedule_job(job_id):
    if sched.get_job(job_id) is not None:
        log.debug("Unscheduling job %s", job_id)
        sched.remove_job(job_id)


def toggle_seedset_inactive(seedset_id):
    try:
        seed_set = SeedSet.objects.get(id=seedset_id)
    except ObjectDoesNotExist:
        log.error("Toggling seedset %s to inactive failed because seedset does not exist", seedset_id)
        return
    log.debug("Toggling seedset %s to inactive and clearing end date.", seedset_id)
    seed_set.is_active = False
    seed_set.end_date = None
    seed_set.save()


def schedule_harvest(seedset_pk, is_active, schedule_minutes, start_date=None, end_date=None):
    assert schedule_minutes

    unschedule_harvest(seedset_pk)
    log.debug("Seedset %s is active = %s", seedset_pk, is_active)
    if is_active:
        name = "Harvest ({}) for seedset {}".format(schedule_minutes, seedset_pk)
        log.debug("Scheduling job %s", name)
        sched.add_job(seedset_harvest,
                      args=[seedset_pk],
                      id=_job_id(seedset_pk),
                      name=name,
                      trigger='interval',
                      start_date=start_date,
                      end_date=end_date,
                      minutes=schedule_minutes)

        if end_date:
            log.debug("Scheduling end job for %s to run at %s", name, end_date)
            sched.add_job(toggle_seedset_inactive,
                          args=[seedset_pk],
                          id=_end_job_id(seedset_pk),
                          name="End harvest for seedset {}".format(seedset_pk),
                          trigger='date',
                          run_date=end_date)


def schedule_stream_harvest(seedset_pk, is_active, start_date=None, end_date=None, last_harvest_status=None):
    unschedule_harvest(seedset_pk)

    log.debug("Seedset %s is active = %s", seedset_pk, is_active)
    if is_active:
        name = "Harvest for seedset {}".format(seedset_pk)
        log.debug("Scheduling job %s", name)
        sched.add_job(seedset_harvest,
                      args=[seedset_pk],
                      id=_job_id(seedset_pk),
                      name=name,
                      trigger='date',
                      run_date=start_date)

        if end_date:
            log.debug("Scheduling end job for %s to run at %s", name, end_date)
            sched.add_job(toggle_seedset_inactive,
                          args=[seedset_pk],
                          id=_end_job_id(seedset_pk),
                          name="End harvest for seedset {}".format(seedset_pk),
                          trigger='date',
                          run_date=end_date)
    # If not active and last harvest requested or running
    elif last_harvest_status in (Harvest.REQUESTED, Harvest.RUNNING):
        log.debug("Stopping seedset %s", seedset_pk)
        seedset_stop(seedset_pk)


def schedule_harvest_receiver(sender, **kwargs):
    assert kwargs["instance"]
    seedset = kwargs["instance"]

    if diff_field_changed(seedset):
        if seedset.is_streaming():
            last_harvest = seedset.last_harvest()
            schedule_stream_harvest(seedset.id, seedset.is_active,
                                    start_date=datetime.datetime.now() + datetime.timedelta(seconds=15),
                                    end_date=seedset.end_date or None,
                                    last_harvest_status=last_harvest.status if last_harvest else None)
        else:
            schedule_harvest(seedset.id, seedset.is_active, seedset.schedule_minutes,
                             start_date=datetime.datetime.now() + datetime.timedelta(seconds=15),
                             end_date=seedset.end_date or None)
    else:
        log.debug("Skipping scheduling harvest of seedset %s since nothing significant changed.", seedset.pk)


def unschedule_harvest_receiver(sender, **kwargs):
    assert kwargs["instance"]
    seedset = kwargs["instance"]

    unschedule_harvest(seedset.id)
