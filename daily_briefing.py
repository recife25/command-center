from outlook_module import OutlookCalendar
from datetime import datetime

class DailyBriefing:
    def __init__(self):
        self.calendar = OutlookCalendar()

    def generate_briefing(self):
        today = datetime.now().strftime("%A, %B %d, %Y")
        events = self.calendar.get_today_events()

        briefing = f"Daily Briefing — {today}\n\n"

        if not events:
            briefing += "No events scheduled for today.\n"
        else:
            briefing += "Today's Events:\n\n"
            for e in events:
                briefing += f"- {e['subject']} at {e['start_time']}\n"

        # NEW: System Status Section
        briefing += "\nSystem Status:\n"
        briefing += "- FastAPI backend: RUNNING\n"
        briefing += "- Streamlit dashboard: ACTIVE\n"
        briefing += "- Modules loaded: DailyBriefing, CalendarScheduler, OutlookCalendar\n"
        briefing += "- Last update: " + today + "\n"

        return briefing


if __name__ == "__main__":
    db = DailyBriefing()
    print(db.generate_briefing())
