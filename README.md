# Task Management CLI

A command-line interface tool for managing users, projects, and tasks with persistent JSON-based storage.

## Project Overview

This is a Python-based OOP project that demonstrates:
- Object-oriented design with Model and Manager classes
- CLI argument parsing with `argparse`
- JSON file persistence
- Comprehensive unit and integration testing
- Mock data testing

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd final-oop-lab
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python main.py --help
   ```

## Project Structure

```
final-oop-lab/
├── main.py                 # CLI entry point
├── models/
│   ├── user.py            # User and UserManager classes
│   ├── project.py         # Project and ProjectManager classes
│   └── task.py            # Task and TaskManager classes
├── utils/
│   └── file_helpers.py    # JSON file I/O utilities
├── data/
│   ├── users.json         # User data storage
│   ├── projects.json      # Project data storage
│   └── tasks.json         # Task data storage
├── tests/
│   ├── test_model.py      # Unit tests for models
│   └── test_cli.py        # CLI and integration tests
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## CLI Commands

### User Management

**Add a new user:**
```bash
python main.py add-user <name> <email>
```
Example:
```bash
python main.py add-user "Alice" "alice@example.com"
```

**List all users:**
```bash
python main.py list-users
```

### Project Management

**Add a new project:**
```bash
python main.py add-project <title> <description> <due_date> <owner_email>
```
Example:
```bash
python main.py add-project "Website Redesign" "Redesign company website" "2025-12-31" "alice@example.com"
```

**List all projects:**
```bash
python main.py list-projects
```

### Task Management

**Add a new task:**
```bash
python main.py add-task <title> <status> [--project_title <title>] [--assigned_to <email>]
```
Examples:
```bash
# Task with all fields
python main.py add-task "Design homepage" "in-progress" --project_title "Website Redesign" --assigned_to "alice@example.com"

# Task with minimal fields
python main.py add-task "Review code" "todo"
```

**List all tasks:**
```bash
python main.py list-tasks
```

## Arguments Reference

### User Commands
- `add-user NAME EMAIL` - Add a new user
  - `NAME`: User's full name (string)
  - `EMAIL`: User's email address (string)

- `list-users` - Display all users

### Project Commands
- `add-project TITLE DESCRIPTION DUE_DATE OWNER` - Add a new project
  - `TITLE`: Project title (string)
  - `DESCRIPTION`: Project description (string)
  - `DUE_DATE`: Due date (string, e.g., "2025-12-31")
  - `OWNER`: Owner's email address (string)

- `list-projects` - Display all projects

### Task Commands
- `add-task TITLE STATUS [OPTIONS]` - Add a new task
  - `TITLE`: Task title (string)
  - `STATUS`: Task status (string, e.g., "todo", "in-progress", "done")
  - `--project_title`: Optional project title (string)
  - `--assigned_to`: Optional assignee email (string)

- `list-tasks` - Display all tasks

## Running Tests

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test file:
```bash
python -m pytest tests/test_model.py -v
python -m pytest tests/test_cli.py -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=models --cov=utils
```

## Test Coverage

- **29 unit and integration tests** covering:
  - Model creation and validation
  - Manager CRUD operations
  - CLI command parsing
  - Data persistence
  - Mock data scenarios
  - Edge cases (unassigned tasks, optional fields)

## Data Storage

All data is stored in JSON files in the `data/` directory:
- `users.json` - User records
- `projects.json` - Project records
- `tasks.json` - Task records

Data persists between CLI invocations.

## Example Workflow

```bash
# Add users
python main.py add-user "Alice" "alice@example.com"
python main.py add-user "Bob" "bob@example.com"

# Add projects
python main.py add-project "Website" "Build website" "2025-12-31" "alice@example.com"

# Add tasks
python main.py add-task "Design UI" "in-progress" --project_title "Website" --assigned_to "alice@example.com"
python main.py add-task "Backend API" "todo" --project_title "Website" --assigned_to "bob@example.com"

# View all data
python main.py list-users
python main.py list-projects
python main.py list-tasks
```

## Dependencies

- `pytest` - Testing framework
- `requests` - HTTP library (included in environment)

See `requirements.txt` for complete list.

## License

This is a Flatiron School project.

