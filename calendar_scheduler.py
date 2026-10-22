from datetime import datetime, timedelta
from outlook_module import OutlookCalendar

class CalendarScheduler:
    def __init__(self):
        self.outlook = OutlookCalendar()

    def get_free_time_blocks(self):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        events = self.outlook.get_events_by_date(tomorrow)

        # Convert events into time ranges
        busy = []
        for e in events:
            start = datetime.fromisoformat(e["start"])
            end = datetime.fromisoformat(e["end"])
            busy.append((start, end))

        # Sort by start time
        busy.sort(key=lambda x: x[0])

        # Define working hours
        day_start = datetime.fromisoformat(tomorrow + "T09:00:00")
        day_end   = datetime.fromisoformat(tomorrow + "T17:00:00")

        free_blocks = []
        current = day_start

        for start, end in busy:
            if current < start:
                free_blocks.append((current, start))
            current = max(current, end)

        if current < day_end:
            free_blocks.append((current, day_end))

        return free_blocks

    def schedule_tasks(self):
        free_blocks = self.get_free_time_blocks()

        if not free_blocks:
            return "No free time tomorrow."

        msg = "Free time blocks tomorrow:\n\n"
        for start, end in free_blocks:
            msg += f"- {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}\n"

        return msg
