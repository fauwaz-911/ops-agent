from datetime import datetime, timezone
from .notion_client import fetch_tasks
from .telegram import send_message


def parse_date(date_str):
    if not date_str:
        return None
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))


def build_reminders():
    tasks = fetch_high_priority_tasks()
    now = datetime.now(timezone.utc)

    reminders = []

    for task in tasks:
        due = parse_date(task["due"])
        if not due:
            continue

        delta = (due - now).total_seconds()

        # --- Conditions ---
        if 0 < delta <= 86400:
            reminders.append(f"⏳ Due within 24h:\n{task['name']}")

        elif 0 < delta <= 10800:
            reminders.append(f"⚠️ Due within 3h:\n{task['name']}")

        elif delta < 0:
            reminders.append(f"🚨 OVERDUE:\n{task['name']}")

    return reminders


def run_reminder_engine():
    reminders = build_reminders()

    if reminders:
        message = "🧠 Smart Task Alerts\n\n" + "\n\n".join(reminders)
        send_telegram_message(message)

