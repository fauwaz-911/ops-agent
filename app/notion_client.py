import os
import requests

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_TASKS_DB_ID")

def fetch_tasks():
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    tasks = []
    for r in data.get("results", []):
        name = r["properties"]["Task Name"]["title"]
        if name:
            tasks.append(name[0]["plain_text"])
    return tasks
