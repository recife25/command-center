the purpose of outlook_calendar_history :
is to be an engineering journal 

# class OutlookCalendar & class OutlookEmail (OLD IMPLEMENTATION)
# from auth import get_token
# import requests

# SEND_URL = "https://graph.microsoft.com/v1.0/me/sendMail"

# def send_email():
#     token = get_token()

#     message = {
#         "message": {
#             "subject": "Command Center Test Email",
#             "body": {
#                 "contentType": "Text",
#                 "content": "This is a test email from your Command Center via Microsoft Graph."
#             },
#             "toRecipients": [
#                 {
#                     "emailAddress": {
#                         "address": "pjfruiz@hotmail.com"
#                     }
#                 }
#             ]
#         }
#     }

#     response = requests.post(
#         SEND_URL,
#         headers={"Authorization": f"Bearer {token}"},
#         json=message
#     )

#     print(response.status_code, response.text)

# if __name__ == "__main__":
#     send_email()


# -------------------------------------------------------------
# Old outlookvcalendar implementation after crud        
# -------------------------------------------------------------

# class OutlookCalendar:
#     def __init__(self):
#         self.token = get_token()
#         self.headers = {"Authorization": f"Bearer {self.token}",
#                         "Content-Type": "application/json"
#                         }

#     def list_events(self):
#         url = f"{GRAPH_BASE}/me/events?$top=10"
#         response = requests.get(url, headers=self.headers)
#         return response.json()


        

#     def get_events(self, date):
#         url = f"{GRAPH_BASE}/me/calendarview?startDateTime={date}T00:00:00&endDateTime={date}T23:59:59"
#         headers = {"Authorization": f"Bearer {self.token}"}
#         response = requests.get(url, headers=headers).json()

#         events = []
#         for e in response.get("value", []):
#             events.append({
#                 "subject": e.get("subject"),
#                 "start": e["start"]["dateTime"],
#                 "end": e["end"]["dateTime"]
#             })
#         return events

#     def create_event(self, title, start, end, description):
#         url = f"{GRAPH_BASE}/me/events"
#         headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/json"
#         }

#         event = {
#             "subject": title,
#             "body": {"contentType": "HTML", "content": description},
#             "start": {"dateTime": start.isoformat(), "timeZone": "America/New_York"},
#             "end": {"dateTime": end.isoformat(), "timeZone": "America/New_York"}
#         }

#         response = requests.post(url, headers=headers, json=event)
#         return response.json()
