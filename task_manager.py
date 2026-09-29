import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        if not os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "w") as f:
                json.dump([], f)
        self.tasks = self.load_tasks()

    def load_tasks(self):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, category="study", due_date=None, estimate=None):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,  # study, lab, homework, reading, project, misc
            "due_date": due_date,
            "estimate": estimate,  # hours or points
            "created_at": datetime.now().isoformat(),
            "completed": False,
            "completed_at": None
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def list_tasks(self, show_completed=False):
        if show_completed:
            return self.tasks
        return [t for t in self.tasks if not t["completed"]]

    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                return task
        return None

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()

    def get_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
