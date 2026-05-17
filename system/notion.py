# system/notion.py

import requests
from system.config import load_env

NOTION_VERSION = "2022-06-28"

def get_new_items():
    env = load_env()

    url = f"https://api.notion.com/v1/databases/{env['NOTION_DATABASE']}/query"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "filter": {
            "property": "Processing status",
            "select": {"equals": "New"}
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка при получении новых задач:", response.text)
        return []

    results = response.json().get("results", [])
    items = []

    for r in results:
        props = r["properties"]

        items.append({
            "id": r["id"],
            "uid": props["Email ID"]["title"][0]["text"]["content"],
            "sender": props["Sender"]["rich_text"][0]["text"]["content"] if props["Sender"]["rich_text"] else "",
            "subject": props["Subject of the letter"]["rich_text"][0]["text"]["content"] if props["Subject of the letter"]["rich_text"] else "",
            "body": props["Summary"]["rich_text"][0]["text"]["content"] if props["Summary"]["rich_text"] else ""
        })

    return items

def update_item(item_id, category, route, status):
    env = load_env()

    url = f"https://api.notion.com/v1/pages/{item_id}"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "properties": {
            "Category": {
                "select": {"name": category}
            },
            "Route": {
                "rich_text": [{"text": {"content": route}}]
            },
            "Processing status": {
                "select": {"name": status}
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка обновления записи:", response.text)

    return response.json()

def get_routed_items(route_name):
    env = load_env()

    url = f"https://api.notion.com/v1/databases/{env['NOTION_DATABASE']}/query"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "filter": {
            "and": [
                {"property": "Processing status", "select": {"equals": "Routed"}},
                {"property": "Route", "rich_text": {"equals": route_name}}
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка при получении задач:", response.text)
        return []

    results = response.json().get("results", [])
    items = []

    for r in results:
        props = r["properties"]

        items.append({
            "id": r["id"],
            "uid": props["Email ID"]["title"][0]["text"]["content"],
            "subject": props["Subject of the letter"]["rich_text"][0]["text"]["content"] if props["Subject of the letter"]["rich_text"] else "",
            "body": props["Summary"]["rich_text"][0]["text"]["content"] if props["Summary"]["rich_text"] else ""
        })

    return items

def update_item_result(item_id, result, status):
    env = load_env()

    url = f"https://api.notion.com/v1/pages/{item_id}"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "properties": {
            "Result": {
                "rich_text": [{"text": {"content": result}}]
            },
            "Processing status": {
                "select": {"name": status}
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка обновления результата:", response.text)

    return response.json()

def get_done_items():
    env = load_env()

    url = f"https://api.notion.com/v1/databases/{env['NOTION_DATABASE']}/query"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "filter": {
            "property": "Processing status",
            "select": {"equals": "Done"}
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка при получении Done-задач:", response.text)
        return []

    results = response.json().get("results", [])
    items = []

    for r in results:
        props = r["properties"]

        items.append({
            "id": r["id"],
            "uid": props["Email ID"]["title"][0]["text"]["content"],
            "sender": props["Sender"]["rich_text"][0]["text"]["content"] if props["Sender"]["rich_text"] else "",
            "subject": props["Subject of the letter"]["rich_text"][0]["text"]["content"] if props["Subject of the letter"]["rich_text"] else "",
            "body": props["Summary"]["rich_text"][0]["text"]["content"] if props["Summary"]["rich_text"] else ""
        })

    return items

def update_reply_status(item_id, status):
    env = load_env()

    url = f"https://api.notion.com/v1/pages/{item_id}"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "properties": {
            "Processing status": {
                "select": {"name": status}
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка обновления статуса ответа:", response.text)

    return response.json()

def get_items_by_status(status):
    env = load_env()

    url = f"https://api.notion.com/v1/databases/{env['NOTION_DATABASE']}/query"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "filter": {
            "property": "Processing status",
            "select": {"equals": status}
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка при получении задач:", response.text)
        return []

    results = response.json().get("results", [])
    items = []

    for r in results:
        props = r["properties"]

        items.append({
        "id": r["id"],
        "uid": props["Email ID"]["title"][0]["text"]["content"],
        "sender": props["Sender"]["rich_text"][0]["text"]["content"] if props["Sender"]["rich_text"] else "",
        "subject": props["Subject of the letter"]["rich_text"][0]["text"]["content"] if props["Subject of the letter"]["rich_text"] else "",
        "body": props["Summary"]["rich_text"][0]["text"]["content"] if props["Summary"]["rich_text"] else "",
        "status": props["Processing status"]["select"]["name"] if props["Processing status"]["select"] else "",
        "result": props["Result"]["rich_text"][0]["text"]["content"] if props.get("Result") and props["Result"]["rich_text"] else ""
    })

    return items

def archive_item(item_id, new_status, archived_at):
    env = load_env()

    url = f"https://api.notion.com/v1/pages/{item_id}"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "properties": {
            "Processing status": {
                "select": {"name": new_status}
            },
            "Archived at": {
                "date": {"start": archived_at}
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка архивации:", response.text)

    return response.json()

def count_items_by_status(status):
    env = load_env()

    url = f"https://api.notion.com/v1/databases/{env['NOTION_DATABASE']}/query"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "filter": {
            "property": "Processing status",
            "select": {"equals": status}
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка при подсчёте:", response.text)
        return 0

    return len(response.json().get("results", []))

def get_processing_times():
    # Здесь можно сделать расширенную аналитику:
    # - время от New → Routed
    # - время от Routed → Done
    # - время от Done → Replied
    # - время от Replied → Archived

    # Пока — заглушка
    return {
        "avg_processing_time": "N/A",
        "avg_reply_time": "N/A"
    }

def write_analytics_report(database_id, report):
    env = load_env()

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Timestamp": {
                "title": [{"text": {"content": report["timestamp"]}}]
            },
            "New": {"number": report["metrics"].get("New", 0)},
            "Routed": {"number": report["metrics"].get("Routed", 0)},
            "Done": {"number": report["metrics"].get("Done", 0)},
            "Replied": {"number": report["metrics"].get("Replied", 0)},
            "Archived": {"number": report["metrics"].get("Archived", 0)}
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка записи отчёта:", response.text)

    return response.json()

def get_all_items():
    env = load_env()

    url = f"https://api.notion.com/v1/databases/{env['NOTION_DATABASE']}/query"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {"page_size": 100}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка при получении всех задач:", response.text)
        return []

    results = response.json().get("results", [])
    items = []

    for r in results:
        props = r["properties"]

        items.append({
            "id": r["id"],
            "uid": props["Email ID"]["title"][0]["text"]["content"],
            "status": props["Processing status"]["select"]["name"] if props["Processing status"]["select"] else "",
            "category": props["Category"]["select"]["name"] if props["Category"]["select"] else "",
            "route": props["Route"]["rich_text"][0]["text"]["content"] if props["Route"]["rich_text"] else "",
            "result": props["Result"]["rich_text"][0]["text"]["content"] if props["Result"]["rich_text"] else "",
            "reply": props["Reply"]["rich_text"][0]["text"]["content"] if props.get("Reply") and props["Reply"]["rich_text"] else ""
        })

    return items

def write_qa_report(database_id, report):
    env = load_env()

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    issues_text = "\n".join(report["issues"]) if report["issues"] else "Нет проблем"

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Timestamp": {
                "title": [{"text": {"content": report["timestamp"]}}]
            },
            "Issues count": {"number": report["issues_count"]},
            "Issues": {
                "rich_text": [{"text": {"content": issues_text}}]
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка записи QA отчёта:", response.text)

    return response.json()

def mark_integrated(item_id):
    env = load_env()

    url = f"https://api.notion.com/v1/pages/{item_id}"

    headers = {
        "Authorization": f"Bearer {env['NOTION_TOKEN']}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }

    payload = {
        "properties": {
            "Integrated": {
                "checkbox": True
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[Notion] Ошибка отметки интеграции:", response.text)

    return response.json()

