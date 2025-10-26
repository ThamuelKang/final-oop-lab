import unittest
import sys
import os
import json
import tempfile
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main


class TestCLI(unittest.TestCase):
    """Test cases for CLI commands"""

    def setUp(self):
        """Set up test fixtures with mock data"""
        self.temp_dir = tempfile.mkdtemp()
        self.users_file = Path(self.temp_dir) / "users.json"
        self.projects_file = Path(self.temp_dir) / "projects.json"
        self.tasks_file = Path(self.temp_dir) / "tasks.json"

        # Create mock data
        self.mock_users = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"}
        ]

        self.mock_projects = [
            {
                "title": "Website Redesign",
                "description": "Redesign company website",
                "due_date": "2025-12-31",
                "owner_email": "alice@example.com"
            },
            {
                "title": "Mobile App",
                "description": "Build iOS app",
                "due_date": "2025-06-30",
                "owner_email": "bob@example.com"
            }
        ]

        self.mock_tasks = [
            {
                "title": "Design homepage",
                "status": "in-progress",
                "project_title": "Website Redesign",
                "assigned_to": "alice@example.com"
            },
            {
                "title": "Setup project",
                "status": "todo",
                "project_title": "Mobile App",
                "assigned_to": "bob@example.com"
            },
            {
                "title": "Review code",
                "status": "todo",
                "project_title": None,
                "assigned_to": None
            }
        ]

        # Write mock data to files
        self.users_file.write_text(json.dumps(self.mock_users, indent=4))
        self.projects_file.write_text(json.dumps(self.mock_projects, indent=4))
        self.tasks_file.write_text(json.dumps(self.mock_tasks, indent=4))

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_users(self, mock_stdout):
        """Test listing users"""
        with patch('models.user.DATA_FILE_PATH', self.users_file):
            with patch('sys.argv', ['main.py', 'list-users']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Alice", output)
        self.assertIn("alice@example.com", output)
        self.assertIn("Bob", output)
        self.assertIn("bob@example.com", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_user(self, mock_stdout):
        """Test adding a user"""
        with patch('models.user.DATA_FILE_PATH', self.users_file):
            with patch('sys.argv', ['main.py', 'add-user', 'Charlie', 'charlie@example.com']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Added user", output)
        self.assertIn("Charlie", output)
        self.assertIn("charlie@example.com", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_projects(self, mock_stdout):
        """Test listing projects"""
        with patch('models.project.PROJECT_DATA_PATH', self.projects_file):
            with patch('sys.argv', ['main.py', 'list-projects']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Website Redesign", output)
        self.assertIn("2025-12-31", output)
        self.assertIn("alice@example.com", output)
        self.assertIn("Mobile App", output)
        self.assertIn("2025-06-30", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_project(self, mock_stdout):
        """Test adding a project"""
        with patch('models.project.PROJECT_DATA_PATH', self.projects_file):
            with patch('sys.argv', ['main.py', 'add-project', 'New Project', 'Description', '2025-12-31', 'owner@example.com']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Added project", output)
        self.assertIn("New Project", output)
        self.assertIn("2025-12-31", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_tasks(self, mock_stdout):
        """Test listing tasks"""
        with patch('models.task.TASK_FILE_PATH', self.tasks_file):
            with patch('sys.argv', ['main.py', 'list-tasks']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Design homepage", output)
        self.assertIn("in-progress", output)
        self.assertIn("Setup project", output)
        self.assertIn("Review code", output)
        self.assertIn("Unassigned", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_task_with_all_fields(self, mock_stdout):
        """Test adding a task with all fields"""
        with patch('models.task.TASK_FILE_PATH', self.tasks_file):
            with patch('sys.argv', ['main.py', 'add-task', 'New Task', 'todo', '--project_title', 'Website Redesign', '--assigned_to', 'alice@example.com']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Added task", output)
        self.assertIn("New Task", output)
        self.assertIn("todo", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_task_minimal(self, mock_stdout):
        """Test adding a task with minimal fields"""
        with patch('models.task.TASK_FILE_PATH', self.tasks_file):
            with patch('sys.argv', ['main.py', 'add-task', 'Minimal Task', 'todo']):
                main()

        output = mock_stdout.getvalue()
        self.assertIn("Added task", output)
        self.assertIn("Minimal Task", output)
        self.assertIn("Unassigned", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        """Test help command"""
        with patch('sys.argv', ['main.py', '--help']):
            try:
                main()
            except SystemExit:
                pass  # --help causes sys.exit(0)

        output = mock_stdout.getvalue()
        self.assertIn("CLI tool to manage users, projects, and tasks", output)
        self.assertIn("add-user", output)
        self.assertIn("list-users", output)
        self.assertIn("add-project", output)
        self.assertIn("list-projects", output)
        self.assertIn("add-task", output)
        self.assertIn("list-tasks", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_command(self, mock_stdout):
        """Test running with no command shows help"""
        with patch('sys.argv', ['main.py']):
            main()

        output = mock_stdout.getvalue()
        self.assertIn("usage:", output)


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Create data directory
        Path("data").mkdir(exist_ok=True)
        Path("data/users.json").write_text("[]")
        Path("data/projects.json").write_text("[]")
        Path("data/tasks.json").write_text("[]")

    def tearDown(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_full_workflow(self):
        """Test a complete workflow: add user, project, and task"""
        # Add user
        result = subprocess.run(
            ['python', os.path.join(self.original_cwd, 'main.py'), 'add-user', 'TestUser', 'test@example.com'],
            capture_output=True,
            text=True,
            cwd=self.original_cwd
        )
        self.assertIn("Added user", result.stdout)

        # Add project
        result = subprocess.run(
            ['python', os.path.join(self.original_cwd, 'main.py'), 'add-project', 'TestProject', 'Test Description', '2025-12-31', 'test@example.com'],
            capture_output=True,
            text=True,
            cwd=self.original_cwd
        )
        self.assertIn("Added project", result.stdout)

        # Add task
        result = subprocess.run(
            ['python', os.path.join(self.original_cwd, 'main.py'), 'add-task', 'TestTask', 'todo'],
            capture_output=True,
            text=True,
            cwd=self.original_cwd
        )
        self.assertIn("Added task", result.stdout)


if __name__ == '__main__':
    unittest.main()
