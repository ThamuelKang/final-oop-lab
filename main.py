import argparse
from models.user import UserManager
from models.project import ProjectManager
from models.task import TaskManager

def main():

    # Instantiate managers
    um = UserManager()
    pm = ProjectManager()
    tm = TaskManager()

    # Create main parser
    parser = argparse.ArgumentParser(description="CLI tool to manage users, projects, and tasks")
    subparsers = parser.add_subparsers(dest="command")

    # User commands
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("name", help="Name of the user")
    add_user_parser.add_argument("email", help="Email of the user")

    list_user_parser = subparsers.add_parser("list-users", help="List all users")

    # Project commands
    add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
    add_project_parser.add_argument("title", help="Project title")
    add_project_parser.add_argument("description", help="Project description")
    add_project_parser.add_argument("due_date", help="Project due date")
    add_project_parser.add_argument("owner", help="Owner email")

    list_project_parser = subparsers.add_parser("list-projects", help="List all projects")

    # Task commands
    add_task_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_task_parser.add_argument("title", help="Task title")
    add_task_parser.add_argument("status", help="Task status")
    add_task_parser.add_argument("--project_title", help="Project title", default=None)
    add_task_parser.add_argument("--assigned_to", help="Assigned user email", default=None)

    list_task_parser = subparsers.add_parser("list-tasks", help="List all tasks")

    # Parse the CLI arguments
    args = parser.parse_args()

    # Method routing!
    if args.command == "add-user":
        um.add_user(args.name, args.email)
    elif args.command == "list-users":
        um.list_users()

    elif args.command == "add-project":
        pm.add_project(args.title, args.description, args.due_date, args.owner)
    elif args.command == "list-projects":
        pm.list_projects()

    elif args.command == "add-task":
        tm.add_task(args.title, args.status, args.project_title, args.assigned_to)
    elif args.command == "list-tasks":
        tm.list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
