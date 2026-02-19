from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .notion_client import fetch_tasks
from .telegram import send_message

scheduler = BackgroundScheduler()
scheduler.add_job(
    run_reminder_engine,
    "interval",
    minutes=30
)


def morning_job():
    tasks = fetch_tasks()
    message = "🌅 Morning Brief\n"
    message += "\n".join(tasks) if tasks else "No tasks."
    send_message(message)

def evening_job():
    tasks = fetch_tasks()
    message = "🌙 Evening Wrap-up\n"
    message += "\n".join(tasks) if tasks else "No tasks."
    send_message(message)

def start_scheduler():
   
    scheduler.add_job(morning_job, 'cron', hour=10, minute=0)
    scheduler.add_job(evening_job, 'cron', hour=18, minute=0)
    scheduler.start()
    scheduler.add_job( run_reminder_engine, "interval", minutes=30) #new
