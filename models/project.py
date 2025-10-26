from pathlib import Path
import json

# Stores path as object using Path()
PROJECT_DATA_PATH = Path("data/projects.json")

# Project class
class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date

    def __str__(self):
        return f"project title: {self.title} is about {self.description} and is due {self.due_date}"

# Manage project class
class ProjectManager:
    def __init__(self):
        self.projects = self.load_projects()

    # Load projects
    def load_projects(self):

        try:
            with open(PROJECT_DATA_PATH, "r") as file:

                # Converts it from JSON -> Python Objects
                data = json.load(file)

                # Converts Python Objects and creates Project()
                projects = []
                for proj in data:
                    title = proj["title"]
                    description = proj["description"]
                    due_date = proj["due_date"]
                    project = Project(title, description, due_date)
                    projects.append(project)
                return projects
        except FileNotFoundError:
            print("File not found, returning an empty lists")
            return []
        except json.JSONDecodeError:
            print("JSON format is bad, returning an empty list")
            return []

    # Saving logic
    def save_projects(self):
        saved_data = []

        for proj in self.projects:
            proj_dictionary = {
                "title": proj.title,
                "description": proj.description,
                "due_date": proj.due_date,
            }
            saved_data.append(proj_dictionary)

        # Must overwrite and need JSON formatting!
        with open(PROJECT_DATA_PATH, "w") as file:
            json.dump(saved_data, file, indent=2)

    # Add project functionality
    def add_project(self, title, description, due_date):
        new_project = Project(title, description, due_date)
        self.projects.append(new_project)
        self.save_projects()
        print(
            f"{new_project.description} ({new_project.description} due on {new_project.due_date}) has been added"
        )

    # Lists all projects
    def lists_projects(self):
        for proj in self.projects:
            print(proj)