

import requests
from auth import get_token

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# ---------------------------------------------
# NEW OUTLOOKCALENDAR CRUD (REPLACE YOUR OLD ONE)
#----------------------------------------------

class OutlookCalendar:
    def __init__(self):
        self.token = get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # ---------------------------------------------------------
    # CREATE EVENT
    # ---------------------------------------------------------
    def create_event(self, title, start, end, description=""):
        url = f"{GRAPH_BASE}/me/events"

        event = {
            "subject": title,
            "body": {"contentType": "text", "content": description},
            "start": {"dateTime": start.isoformat(), "timeZone": "America/New_York"},
            "end": {"dateTime": end.isoformat(), "timeZone": "America/New_York"}
        }

        response = requests.post(url, headers=self.headers, json=event)
        return response.json()

    # ---------------------------------------------------------
    # READ EVENTS (LIST)
    # ---------------------------------------------------------
    def list_events(self, top=10):
        url = f"{GRAPH_BASE}/me/events?$top={top}"
        response = requests.get(url, headers=self.headers)
        return response.json().get("value", [])

    # ---------------------------------------------------------
    # READ EVENTS BY DATE
    # ---------------------------------------------------------
    def get_events_by_date(self, date):
        """
        date format: YYYY-MM-DD
        """
        url = (
            f"{GRAPH_BASE}/me/calendarview?"
            f"startDateTime={date}T00:00:00&endDateTime={date}T23:59:59"
        )

        response = requests.get(url, headers=self.headers).json()
        events = []

        for e in response.get("value", []):
            events.append({
                "id": e.get("id"),
                "subject": e.get("subject"),
                "start": e["start"]["dateTime"],
                "end": e["end"]["dateTime"]
            })

        return events

    # ---------------------------------------------------------
    # GET EVENT BY ID
    # ---------------------------------------------------------
    def get_event(self, event_id):
        url = f"{GRAPH_BASE}/me/events/{event_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    # ---------------------------------------------------------
    # UPDATE EVENT
    # ---------------------------------------------------------
    def update_event(self, event_id, title=None, start=None, end=None, description=None):
        url = f"{GRAPH_BASE}/me/events/{event_id}"

        update_payload = {}

        if title:
            update_payload["subject"] = title

        if description:
            update_payload["body"] = {"contentType": "text", "content": description}

        if start:
            update_payload["start"] = {
                "dateTime": start.isoformat(),
                "timeZone": "America/New_York"
            }

        if end:
            update_payload["end"] = {
                "dateTime": end.isoformat(),
                "timeZone": "America/New_York"
            }

        response = requests.patch(url, headers=self.headers, json=update_payload)
        return response.json()

    # ---------------------------------------------------------
    # DELETE EVENT
    # ---------------------------------------------------------
    def delete_event(self, event_id):
        url = f"{GRAPH_BASE}/me/events/{event_id}"
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            return {"status": "deleted"}
        else:
            return {"status": "error", "details": response.text}
        


class OutlookEmail:
    def __init__(self):
        self.token = get_token()

    def send_email(self, subject, body):
        url = f"{GRAPH_BASE}/me/sendMail"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        message = {
            "message": {
                "subject": subject,
                "body": {"contentType": "text", "content": body},
                "toRecipients": [{"emailAddress": {"address": "<YOUR_EMAIL>"}}]
            }
        }

        response = requests.post(url, headers=headers, json=message)
        return response.json()

