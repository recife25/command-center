from outlook_module import OutlookCalendar
from calendar_scheduler import CalendarScheduler
from daily_briefing import DailyBriefing

class CommandCenterOrchestrator:
    def __init__(self):
        self.outlook = OutlookCalendar()
        self.scheduler = CalendarScheduler()
        self.briefing = DailyBriefing()

    # ---------------------------------------------------------
    # MORNING ROUTINE (BAREBONE)
    # ---------------------------------------------------------
    def run_morning_routine(self):
        print("Running Morning Routine...\n")

        # Daily briefing
        briefing = self.briefing.generate_briefing()
        print(briefing)

        # Smart calendar scheduling
        print(self.scheduler.schedule_tasks())

        print("\nMorning routine complete.\n")
        return "Morning routine executed."

    # ---------------------------------------------------------
    # RUN EVERYTHING (BAREBONE)
    # ---------------------------------------------------------
    def run_all(self):
        print("Running FULL Command Center...\n")

        print(self.run_morning_routine())

        print("\nFULL Command Center execution complete.\n")
        return "All routines executed."


if __name__ == "__main__":
    cc = CommandCenterOrchestrator()
    print(cc.run_all())

