import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User, UserManager
from models.project import Project, ProjectManager
from models.task import Task, TaskManager


class TestUser(unittest.TestCase):
    """Test cases for User model"""

    def test_user_creation(self):
        """Test creating a user"""
        user = User("John Doe", "john@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.projects, [])

    def test_user_add_project(self):
        """Test adding a project to a user"""
        user = User("Jane Doe", "jane@example.com")
        project = Project("Test Project", "A test project", "2025-12-31", "jane@example.com")
        user.add_project(project)
        self.assertEqual(len(user.projects), 1)
        self.assertIn(project, user.projects)

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User("Alice", "alice@example.com")
        self.assertEqual(str(user), "Alice (alice@example.com)")


class TestProject(unittest.TestCase):
    """Test cases for Project model"""

    def test_project_creation(self):
        """Test creating a project"""
        project = Project("Website", "Build a website", "2025-12-31", "owner@example.com")
        self.assertEqual(project.title, "Website")
        self.assertEqual(project.description, "Build a website")
        self.assertEqual(project.due_date, "2025-12-31")
        self.assertEqual(project.owner_email, "owner@example.com")
        self.assertEqual(project.tasks, [])

    def test_project_add_task(self):
        """Test adding a task to a project"""
        project = Project("App", "Build an app", "2025-06-30", "dev@example.com")
        task = Task("Design UI", "todo", "App", "dev@example.com")
        project.add_task(task)
        self.assertEqual(len(project.tasks), 1)
        self.assertIn(task, project.tasks)

    def test_project_str_representation(self):
        """Test project string representation"""
        project = Project("Mobile App", "iOS app", "2025-06-30", "bob@example.com")
        expected = "Mobile App (due 2025-06-30) owned by bob@example.com"
        self.assertEqual(str(project), expected)


class TestTask(unittest.TestCase):
    """Test cases for Task model"""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields"""
        task = Task("Write tests", "in-progress", "Project X", "dev@example.com")
        self.assertEqual(task.title, "Write tests")
        self.assertEqual(task.status, "in-progress")
        self.assertEqual(task.project_title, "Project X")
        self.assertEqual(task.assigned_to, "dev@example.com")

    def test_task_creation_with_optional_fields(self):
        """Test creating a task without optional fields"""
        task = Task("Review code", "todo", None, None)
        self.assertEqual(task.title, "Review code")
        self.assertEqual(task.status, "todo")
        self.assertIsNone(task.project_title)
        self.assertIsNone(task.assigned_to)

    def test_task_str_representation_with_assignment(self):
        """Test task string representation with assignment"""
        task = Task("Deploy", "done", "Release", "admin@example.com")
        expected = "Deploy [done] assigned to admin@example.com (Project: Release)"
        self.assertEqual(str(task), expected)

    def test_task_str_representation_unassigned(self):
        """Test task string representation when unassigned"""
        task = Task("Backlog item", "todo", None, None)
        expected = "Backlog item [todo] assigned to Unassigned (Project: None)"
        self.assertEqual(str(task), expected)


class TestUserManager(unittest.TestCase):
    """Test cases for UserManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = Path(self.temp_dir) / "users.json"
        self.temp_file.write_text("[]")

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    @patch('models.user.DATA_FILE_PATH')
    def test_load_users_empty(self, mock_path):
        """Test loading users from empty file"""
        mock_path.__str__ = lambda x: str(self.temp_file)
        mock_path.__truediv__ = lambda x, y: self.temp_file

        with patch('models.user.load_json', return_value=[]):
            manager = UserManager()
            self.assertEqual(len(manager.users), 0)

    @patch('models.user.DATA_FILE_PATH')
    @patch('models.user.load_json')
    def test_load_users_with_data(self, mock_load, mock_path):
        """Test loading users with data"""
        mock_load.return_value = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"}
        ]

        manager = UserManager()
        self.assertEqual(len(manager.users), 2)
        self.assertEqual(manager.users[0].name, "Alice")
        self.assertEqual(manager.users[1].email, "bob@example.com")

    @patch('models.user.save_json')
    @patch('models.user.load_json', return_value=[])
    def test_add_user(self, mock_load, mock_save):
        """Test adding a user"""
        manager = UserManager()
        manager.add_user("Charlie", "charlie@example.com")

        self.assertEqual(len(manager.users), 1)
        self.assertEqual(manager.users[0].name, "Charlie")
        mock_save.assert_called_once()


class TestProjectManager(unittest.TestCase):
    """Test cases for ProjectManager"""

    @patch('models.project.load_json')
    def test_load_projects_empty(self, mock_load):
        """Test loading projects from empty file"""
        mock_load.return_value = []
        manager = ProjectManager()
        self.assertEqual(len(manager.projects), 0)

    @patch('models.project.load_json')
    def test_load_projects_with_data(self, mock_load):
        """Test loading projects with data"""
        mock_load.return_value = [
            {
                "title": "Website",
                "description": "Build website",
                "due_date": "2025-12-31",
                "owner_email": "owner@example.com"
            }
        ]

        manager = ProjectManager()
        self.assertEqual(len(manager.projects), 1)
        self.assertEqual(manager.projects[0].title, "Website")
        self.assertEqual(manager.projects[0].owner_email, "owner@example.com")

    @patch('models.project.save_json')
    @patch('models.project.load_json', return_value=[])
    def test_add_project(self, mock_load, mock_save):
        """Test adding a project"""
        manager = ProjectManager()
        manager.add_project("App", "Build app", "2025-06-30", "dev@example.com")

        self.assertEqual(len(manager.projects), 1)
        self.assertEqual(manager.projects[0].title, "App")
        mock_save.assert_called_once()


class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = Path(self.temp_dir) / "tasks.json"
        self.temp_file.write_text("[]")

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_tasks_empty(self):
        """Test loading tasks from empty file"""
        with patch('models.task.TASK_FILE_PATH', self.temp_file):
            manager = TaskManager()
            self.assertEqual(len(manager.tasks), 0)

    def test_load_tasks_with_data(self):
        """Test loading tasks with data"""
        task_data = [
            {
                "title": "Task 1",
                "status": "todo",
                "project_title": "Project A",
                "assigned_to": "user@example.com"
            }
        ]
        self.temp_file.write_text(json.dumps(task_data))

        with patch('models.task.TASK_FILE_PATH', self.temp_file):
            manager = TaskManager()
            self.assertEqual(len(manager.tasks), 1)
            self.assertEqual(manager.tasks[0].title, "Task 1")

    def test_add_task(self):
        """Test adding a task"""
        with patch('models.task.TASK_FILE_PATH', self.temp_file):
            manager = TaskManager()
            manager.add_task("New Task", "todo", "Project", "user@example.com")

            self.assertEqual(len(manager.tasks), 1)
            self.assertEqual(manager.tasks[0].title, "New Task")


if __name__ == '__main__':
    unittest.main()
