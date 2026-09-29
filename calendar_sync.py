from auth import get_token
import requests
from outlook_module import OutlookCalendar

GRAPH_URL = "https://graph.microsoft.com/v1.0/me/events"

def create_event():
    token = get_token()

    event = {
        "subject": "Command Center Test Event",
        "start": {
            "dateTime": "2026-09-26T15:00:00",
            "timeZone": "America/New_York"
        },
        "end": {
            "dateTime": "2026-09-26T16:00:00",
            "timeZone": "America/New_York"
        }
    }

    response = requests.post(
        GRAPH_URL,
        headers={"Authorization": f"Bearer {token}"},
        json=event
    )

    print(response.status_code, response.json())

if __name__ == "__main__":
    create_event()
