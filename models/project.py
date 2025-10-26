from pathlib import Path
from utils.file_helpers import load_json, save_json

PROJECT_DATA_PATH = Path("data/projects.json")


class Project:
    def __init__(self, title, description, due_date, owner_email):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_email = owner_email
        
        # holds Task objects
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def __str__(self):
        return f"{self.title} (due {self.due_date}) owned by {self.owner_email}"


class ProjectManager:
    def __init__(self):
        self.projects = self.load_projects()

    def load_projects(self):
        data = load_json(PROJECT_DATA_PATH)
        return [Project(p["title"], p["description"], p["due_date"], p["owner_email"]) for p in data]

    def save_projects(self):
        data = [
            {"title": p.title, "description": p.description, "due_date": p.due_date, "owner_email": p.owner_email}
            for p in self.projects
        ]
        save_json(PROJECT_DATA_PATH, data)

    def add_project(self, title, description, due_date, owner_email):
        new_project = Project(title, description, due_date, owner_email)
        self.projects.append(new_project)
        self.save_projects()
        print(f"Added project: {new_project}")

    def list_projects(self):
        for proj in self.projects:
            print(proj)
