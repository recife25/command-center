# from daily_briefing import DailyBriefing
# from daily_review import DailyReview
# from weekly_review import WeeklyReview
# from progress_tracker import ProgressTracker
# from calendar_scheduler import CalendarScheduler
# from outlook_email_summary import OutlookEmailSummary
# from datetime import datetime

# class CommandCenterOrchestrator:
#     def __init__(self):
#         self.db = DailyBriefing()
#         self.dr = DailyReview()
#         self.wr = WeeklyReview()
#         self.pt = ProgressTracker()
#         self.cs = CalendarScheduler()
#         self.oes = OutlookEmailSummary()

from outlook_module import OutlookCalendar
from calendar_scheduler import CalendarScheduler
from daily_briefing import DailyBriefing
from progress_tracker import ProgressTracker
from weekly_review import WeeklyReview

class CommandCenterOrchestrator:
    def __init__(self):
        self.outlook = OutlookCalendar()
        self.scheduler = CalendarScheduler()
        self.briefing = DailyBriefing()
        self.progress = ProgressTracker()
        self.weekly = WeeklyReview()



    # ---------------------------------------------------------
    # MORNING ROUTINE
    # ---------------------------------------------------------
    def run_morning_routine(self):
        print("Running Morning Routine...\n")

        # Daily briefing
        briefing = self.briefing.generate_briefing()
        print(briefing)

        # Smart calendar scheduling
        print(self.scheduler.schedule_tasks())

        # Daily summary email (morning plan)
        print(self.oes.send_daily_summary())

        print("\nMorning routine complete.\n")
        return "Morning routine executed."


    # ---------------------------------------------------------
    # EVENING ROUTINE
    # ---------------------------------------------------------
    def run_evening_routine(self):
        print("Running Evening Routine...\n")

        # Daily review
        review = self.dr.generate_review()
        print(review)

        # Consistency reminder
        print(self.oes.send_consistency_reminder())

        print("\nEvening routine complete.\n")
        return "Evening routine executed."

    # ---------------------------------------------------------
    # WEEKLY ROUTINE
    # ---------------------------------------------------------
    def run_weekly_routine(self):
        print("Running Weekly Routine...\n")

        # Weekly review
        weekly = self.wr.generate_weekly_review()
        print(weekly)

        # Weekly summary email
        print(self.oes.send_weekly_summary())

        # Overdue alerts
        print(self.oes.send_overdue_alerts())

        print("\nWeekly routine complete.\n")
        return "Weekly routine executed."

    # ---------------------------------------------------------
    # RUN EVERYTHING
    # ---------------------------------------------------------
    def run_all(self):
        print("Running FULL Command Center...\n")

        print(self.run_morning_routine())
        print(self.run_evening_routine())
        print(self.run_weekly_routine())

        print("\nFULL Command Center execution complete.\n")
        return "All routines executed."


if __name__ == "__main__":
    cc = CommandCenterOrchestrator()
    print(cc.run_all())
