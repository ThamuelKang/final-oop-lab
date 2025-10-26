from pathlib import Path
from utils.file_helpers import load_json, save_json

TASK_DATA_PATH = Path("data/tasks.json")


class Task:
    def __init__(self, title, status, assigned_to=None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    def __str__(self):
        assigned = self.assigned_to if self.assigned_to else "unassigned"
        return f"Task: {self.title} | Status: {self.status} | Assigned to: {assigned}"


class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        data = load_json(TASK_DATA_PATH)
        return [Task(t["title"], t["status"], t.get("assigned_to")) for t in data]

    def save_tasks(self):
        data = [{"title": t.title, "status": t.status, "assigned_to": t.assigned_to} 
                for t in self.tasks]
        save_json(TASK_DATA_PATH, data)

    def add_task(self, title, status, assigned_to=None):
        new_task = Task(title, status, assigned_to)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Added task: {new_task}")

    def list_tasks(self):
        for t in self.tasks:
            print(t)
