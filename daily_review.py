from task_manager import TaskManager
from datetime import datetime

class DailyReview:
    def __init__(self):
        self.tm = TaskManager()

    def generate_review(self):
        tasks = self.tm.list_tasks(show_completed=True)
        today = datetime.now().strftime("%A, %B %d, %Y")

        completed = [t for t in tasks if t["completed"]]
        incomplete = [t for t in tasks if not t["completed"]]

        total_estimate_completed = sum(t["estimate"] for t in completed if t["estimate"])
        total_estimate_incomplete = sum(t["estimate"] for t in incomplete if t["estimate"])

        review = f"""
🌙 Daily Review — {today}

Here is your end-of-day summary:

"""

        # Completed tasks
        if completed:
            review += "✅ **Completed Tasks:**\n"
            for t in completed:
                review += f"""
   • {t['title']}
     - Category: {t['category']}
     - Estimate: {t['estimate']} hours
     - Completed at: {t['completed_at']}
"""
        else:
            review += "✅ **Completed Tasks:** None\n"

        # Incomplete tasks
        if incomplete:
            review += "\n⏳ **Incomplete Tasks (carry over to tomorrow):**\n"
            for t in incomplete:
                review += f"""
   • {t['title']}
     - Category: {t['category']}
     - Estimate: {t['estimate']} hours
"""
        else:
            review += "\n⏳ **Incomplete Tasks:** None\n"

        # Summary metrics
        review += f"""

📊 **Daily Metrics**
- Total Completed Time: {total_estimate_completed} hours
- Total Remaining Time: {total_estimate_incomplete} hours
- Daily Velocity: {len(completed)} tasks completed

🎯 **Reflection**
- What went well today?
- What slowed you down?
- What should be adjusted tomorrow?

🔁 **Tomorrow Prep**
- Review incomplete tasks
- Add new tasks if needed
- Plan tomorrow’s study blocks

"""

        return review


if __name__ == "__main__":
    dr = DailyReview()
    print(dr.generate_review())
