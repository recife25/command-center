from task_manager import TaskManager
from datetime import datetime, timedelta
from outlook_module import OutlookCalendar

class WeeklyReview:
    def __init__(self):
        self.tm = TaskManager()
        self.outlook = OutlookCalendar()

    def generate_weekly_review(self):
        tasks = self.tm.list_tasks(show_completed=True)
        today = datetime.now()
        week_start = today - timedelta(days=7)

        completed = [
            t for t in tasks
            if t["completed"] and datetime.fromisoformat(t["completed_at"]) >= week_start
        ]

        incomplete = [
            t for t in tasks
            if not t["completed"]
        ]

        # Category breakdown
        categories = ["study", "lab", "homework", "project", "reading", "misc"]
        category_summary = {c: 0 for c in categories}

        for t in completed:
            if t["category"] in category_summary:
                category_summary[t["category"]] += 1

        # Time totals
        total_completed_time = sum(t["estimate"] for t in completed if t["estimate"])
        total_remaining_time = sum(t["estimate"] for t in incomplete if t["estimate"])

        # Velocity
        weekly_velocity = len(completed)

        # Progress bars (text-based)
        def progress_bar(count):
            filled = "█" * count
            empty = "░" * (10 - count if count < 10 else 0)
            return filled + empty

        review = f"""
📆 **Weekly Review — Week Ending {today.strftime('%A, %B %d, %Y')}**

Here is your full weekly sprint summary:

============================================================
🏁 **Weekly Velocity:** {weekly_velocity} tasks completed
⏱ **Study Hours Logged:** {total_completed_time} hours
📚 **Remaining Backlog Time:** {total_remaining_time} hours
============================================================

"""

        # Completed tasks
        if completed:
            review += "✅ **Completed This Week:**\n"
            for t in completed:
                review += f"""
   • {t['title']}
     - Category: {t['category']}
     - Estimate: {t['estimate']} hours
     - Completed at: {t['completed_at']}
"""
        else:
            review += "✅ **Completed This Week:** None\n"

        # Incomplete tasks
        review += "\n⏳ **Incomplete Tasks (carry into next sprint):**\n"
        for t in incomplete:
            review += f"""
   • {t['title']}
     - Category: {t['category']}
     - Estimate: {t['estimate']} hours
"""

        # Category breakdown
        review += "\n📊 **Category Breakdown:**\n"
        for c in categories:
            review += f"   • {c.capitalize()}: {category_summary[c]} tasks {progress_bar(category_summary[c])}\n"

        # Reflection
        review += f"""

🧠 **Reflection Questions**
- What went well this week?
- What slowed you down?
- What can be improved next week?
- Which habits helped you the most?

🔮 **Next Week Sprint Plan**
- Review incomplete tasks
- Add new study modules
- Add labs and homework
- Prioritize high‑impact items
- Set realistic daily goals

📌 **Suggested Sprint Goals**
- Complete at least 5 tasks
- Log 6–10 study hours
- Finish 1–2 modules
- Maintain daily consistency

============================================================
Weekly review complete. Prepare your next sprint.
============================================================

"""

        return review


if __name__ == "__main__":
    wr = WeeklyReview()
    print(wr.generate_weekly_review())
