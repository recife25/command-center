from task_manager import TaskManager
from datetime import datetime, timedelta
from outlook_module import OutlookCalendar

class ProgressTracker:
    def __init__(self):
        self.tm = TaskManager()
        self.outlook = OutlookCalendar()

    def calculate_progress(self):
        tasks = self.tm.list_tasks(show_completed=True)

        completed = [t for t in tasks if t["completed"]]
        incomplete = [t for t in tasks if not t["completed"]]

        # Category totals
        categories = ["study", "lab", "homework", "project", "reading", "misc"]
        category_hours = {c: 0 for c in categories}

        for t in completed:
            if t["category"] in category_hours:
                category_hours[t["category"]] += t["estimate"]

        # Total hours
        total_completed_hours = sum(t["estimate"] for t in completed if t["estimate"])
        total_remaining_hours = sum(t["estimate"] for t in incomplete if t["estimate"])

        # Completion percentage
        total_tasks = len(tasks)
        completion_percentage = (len(completed) / total_tasks * 100) if total_tasks > 0 else 0

        # Daily velocity (last 24 hours)
        last_24h = datetime.now() - timedelta(hours=24)
        daily_velocity = len([
            t for t in completed
            if datetime.fromisoformat(t["completed_at"]) >= last_24h
        ])

        # Weekly velocity (last 7 days)
        last_week = datetime.now() - timedelta(days=7)
        weekly_velocity = len([
            t for t in completed
            if datetime.fromisoformat(t["completed_at"]) >= last_week
        ])

        # Momentum score (simple formula)
        momentum = (daily_velocity * 2) + weekly_velocity

        return {
            "completed_tasks": len(completed),
            "incomplete_tasks": len(incomplete),
            "total_completed_hours": total_completed_hours,
            "total_remaining_hours": total_remaining_hours,
            "category_hours": category_hours,
            "completion_percentage": completion_percentage,
            "daily_velocity": daily_velocity,
            "weekly_velocity": weekly_velocity,
            "momentum": momentum
        }

    def generate_report(self):
        data = self.calculate_progress()

        report = f"""
📈 **Progress Tracker Summary**

============================================================
✔ Completed Tasks: {data['completed_tasks']}
⏳ Remaining Tasks: {data['incomplete_tasks']}

⏱ Total Study Hours Logged: {data['total_completed_hours']}
📚 Remaining Backlog Hours: {data['total_remaining_hours']}

📊 Completion Percentage: {data['completion_percentage']:.2f}%

🚀 Daily Velocity: {data['daily_velocity']}
📆 Weekly Velocity: {data['weekly_velocity']}

🔥 Momentum Score: {data['momentum']}
============================================================

📂 **Category Breakdown (Hours Logged)**:IN 
"""
        for cat, hours in data["category_hours"].items():
            report += f"   • {cat.capitalize()}: {hours} hours\n"

        report += "\n============================================================\n"
        report += "Progress tracking complete.\n"
        report += "============================================================\n"

        return report


if __name__ == "__main__":
    pt = ProgressTracker()
    print(pt.generate_report())
