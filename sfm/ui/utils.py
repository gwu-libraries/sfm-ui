from jobs import seedset_harvest
from sched import get_sched
from models import SeedSet

def schedule_harvest(id, schedule, s, e):
    sched = get_sched()

    if sched.get_job(str(id)) is not None:
            sched.remove_job(str(id))

    if schedule=='hourly':
        sched.add_job(lambda: seedset_harvest(id),id=str(id) , trigger='cron',
                      hour='*/1', start_date=s, end_date=e)
    elif schedule=='daily':
        sched.add_job(lambda: seedset_harvest(id),id=str(id), trigger='cron',
                      day='*/1', start_date=s, end_date=e)
    elif schedule=='minutely':
        sched.add_job(lambda: seedset_harvest(id),id=str(id), trigger='cron',
                      minute='*/1', start_date=s, end_date=e)
