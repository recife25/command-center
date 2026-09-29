from task_manager import TaskManager
from progress_tracker import ProgressTracker
from datetime import datetime, timedelta
from outlook_module import OutlookCalendar  # your existing Outlook integration

class CalendarScheduler:
    def __init__(self):
        self.tm = TaskManager()
        self.pt = ProgressTracker()
        self.outlook = OutlookCalendar()

    def get_free_time_blocks(self):
        """Fetch free time from Outlook calendar."""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        events = self.outlook.get_events(tomorrow)
        free_blocks = []

        # Build free time blocks between events
        start_of_day = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 8, 0)
        end_of_day = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 22, 0)

        current = start_of_day

        for event in events:
            if event["start"] > current:
                free_blocks.append((current, event["start"]))
            current = event["end"]

        if current < end_of_day:
            free_blocks.append((current, end_of_day))

        return free_blocks

    def schedule_tasks(self):
        """Smart scheduling based on progress metrics."""
        metrics = self.pt.calculate_progress()
        tasks = self.tm.list_tasks()

        free_blocks = self.get_free_time_blocks()

        # Sort tasks by smart priority
        def smart_priority(task):
            priority_map = {
                "study": 1,
                "lab": 2,
                "homework": 3,
                "project": 4,
                "reading": 5,
                "misc": 6
            }

            base = priority_map.get(task["category"], 99)

            # Overdue tasks get boosted
            overdue_boost = 0
            if task["estimate"] and task["created_at"]:
                created = datetime.fromisoformat(task["created_at"])
                if (datetime.now() - created).days >= 3:
                    overdue_boost = -2

            # Momentum adjustment
            momentum_adjust = -1 if metrics["momentum"] < 3 else 0

            return base + overdue_boost + momentum_adjust

        tasks_sorted = sorted(tasks, key=smart_priority)

        # Schedule tasks into free blocks
        for task in tasks_sorted:
            needed = task["estimate"]
            if needed <= 0:
                continue

            for block_start, block_end in free_blocks:
                block_hours = (block_end - block_start).total_seconds() / 3600

                if block_hours >= needed:
                    self.outlook.create_event(
                        title=f"{task['category'].capitalize()} Block — {task['title']}",
                        start=block_start,
                        end=block_start + timedelta(hours=needed),
                        description=f"Auto‑scheduled by Command Center. Estimate: {needed} hours."
                    )
                    break

        return "Smart scheduling complete."

if __name__ == "__main__":
    cs = CalendarScheduler()
    print(cs.schedule_tasks())
