import json
from pathlib import Path

TASK_FILE_PATH = Path("data/tasks.json")

# Task class
class Task:
    def __init__(self, title, status="todo", assigned_to=None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to

    def __str__(self):
        assigned = self.assigned_to if self.assigned_to else "Unassigned"
        return f"Task: {self.title} | Status: {self.status} | Assigned to: {assigned}"

# Task Manager
class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    # Load tasks
    def load_tasks(self):
        try:
            with open(TASK_FILE_PATH, "r") as file:
                
                # Converts it from JSON -> Python Objects
                data = json.load(file)

                return [Task(t["title"], t["status"], t.get("assigned_to")) for t in data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Task file not found or invalid, returning empty list")
            return []

    # Saving logic
    def save_tasks(self):
        with open(TASK_FILE_PATH, "w") as file:
            json.dump(
                [{"title": t.title, "status": t.status, "assigned_to": t.assigned_to} for t in self.tasks],
                file,
                indent=2,
            )

    def add_task(self, title, status="todo", assigned_to=None):
        new_task = Task(title, status, assigned_to)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Added task: {new_task}")

    def list_tasks(self):
        for task in self.tasks:
            print(task)
