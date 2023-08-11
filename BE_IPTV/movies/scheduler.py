from apscheduler.schedulers.background import BackgroundScheduler
from .update import update_database


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_database, 'interval', seconds=30)
    scheduler.start()