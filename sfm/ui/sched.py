from apscheduler.schedulers.background import BackgroundScheduler
import logging

log = logging.getLogger(__name__)

log.debug("Instantiating scheduler")
sched = BackgroundScheduler()


def get_sched():
    return sched


def start_sched():
    log.info("Starting scheduler")
    sched.start()
