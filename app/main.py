from fastapi import FastAPI
from .scheduler import start_scheduler
from .notion_client import fetch_tasks
from .telegram import send_message
from .reminder_engine import run_reminder_engine

from .scheduler import morning_job, evening_job #newest

app = FastAPI()


'''
@app.get("/force-reminder")
def force_reminder():
    run_reminder_engine()
    return {"status": "Reminder executed"}

@app.get("/force-evening")
def force_evening():
    evening_job()
    return {"status": "Evening job executed"}

@app.get("/force-morning")
def force_morning():
    morning_job()
    return {"status": "Morning job executed"}  '''


@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/send-update")
async def send_update():
    tasks = fetch_tasks()
    if not tasks:
        message = "🔔 Ops Update\nNo high-priority tasks."
    else:
        lines = ["🔔 Ops Update", ""]
        for i, t in enumerate(tasks, 1):
            lines.append(f"{i}. {t}")
        message = "\n".join(lines)

    send_message(message)
    return {"status": "sent"}

@app.get("/force-reminder")
async def force_reminder():
    run_reminder_engine()
    return {"status": "Reminder engine executed"}

