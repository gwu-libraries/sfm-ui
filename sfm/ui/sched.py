from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from django.conf import settings
import logging
from jobs import seedset_harvest
import datetime

log = logging.getLogger(__name__)

log.debug("Instantiating scheduler")
sched = BackgroundScheduler()


def start_sched():
    sched.configure(jobstores={
        'default': SQLAlchemyJobStore(url=settings.SCHEDULER_DB_URL)
    })
    log.info("Starting scheduler")
    sched.start()


def next_run_time(seedset_id):
    job_id = str(seedset_id)
    job = sched.get_job(job_id)
    if job:
        return job.next_run_time
    else:
        return None


def unschedule_harvest(seedset_id):
    job_id = str(seedset_id)
    if sched.get_job(job_id) is not None:
        log.debug("Unscheduling job %s", job_id)
        sched.remove_job(job_id)


def schedule_harvest(seedset_id, is_active, schedule_minutes, start_date=None, end_date=None):
    assert schedule_minutes

    unschedule_harvest(seedset_id)
    log.debug("Seedset %s is active = %s", seedset_id, is_active)
    if is_active:
        name = "Harvest ({}) for seedset {}".format(schedule_minutes, seedset_id)
        log.debug("Scheduling job %s", name)
        sched.add_job(seedset_harvest,
                  args=[seedset_id],
                  id=str(seedset_id),
                  name=name,
                  trigger='interval',
                  start_date=start_date,
                  end_date=end_date,
                  minutes=schedule_minutes)


def schedule_harvest_receiver(sender, **kwargs):
    assert kwargs["instance"]
    seedset = kwargs["instance"]

    schedule_harvest(seedset.id, seedset.is_active, seedset.schedule_minutes,
                     start_date=seedset.start_date or datetime.datetime.now() + datetime.timedelta(seconds=15),
                     end_date=seedset.end_date or None)


def unschedule_harvest_receiver(sender, **kwargs):
    assert kwargs["instance"]
    seedset = kwargs["instance"]

    unschedule_harvest(seedset.id)
