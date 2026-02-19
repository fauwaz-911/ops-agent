from fastapi import FastAPI
from .scheduler import start_scheduler
from .notion_client import fetch_tasks
from .telegram import send_message

app = FastAPI()

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