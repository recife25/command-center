from task_manager import TaskManager
from datetime import datetime
from outlook_module import OutlookCalendar

class DailyBriefing:
    def __init__(self):
        self.tm = TaskManager()
        self.outlook = OutlookCalendar()

    def generate_briefing(self):
        tasks = self.tm.list_tasks()
        today = datetime.now().strftime("%A, %B %d, %Y")

        if not tasks:
            return f"""
📅 Daily Briefing — {today}

You have **no tasks** scheduled for today.
This is a good day to:
- Review your backlog
- Add new study tasks
- Plan your next sprint
"""

        # Sort tasks by category priority
        priority_order = {
            "study": 1,
            "lab": 2,
            "homework": 3,
            "project": 4,
            "reading": 5,
            "misc": 6
        }

        tasks_sorted = sorted(tasks, key=lambda t: priority_order.get(t["category"], 99))

        total_estimate = sum(t["estimate"] for t in tasks_sorted if t["estimate"])

        briefing = f"""
📅 Daily Briefing — {today}

Here is your plan for today:

"""

        for t in tasks_sorted:
            briefing += f"""
🔹 **{t['title']}**
   - Category: {t['category']}
   - Estimate: {t['estimate']} hours
   - Created: {t['created_at']}
"""

        briefing += f"""

⏱ **Total Estimated Time:** {total_estimate} hours

⭐ **Suggested Order:**
1. Study tasks first (deep work)
2. Labs second (hands-on)
3. Homework third (reinforcement)
4. Misc last (cleanup)

⚠️ **Blockers:** (manual for now)
- Add blockers here if needed

🎯 **Daily Goal:**
Complete at least 2 tasks and log progress.

"""

        return briefing


if __name__ == "__main__":
    db = DailyBriefing()
    print(db.generate_briefing())
