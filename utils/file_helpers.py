from pathlib import Path
import json

TASK_DATA_PATH = Path("data/tasks.json")

# Load JSON file
def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save JSON file
def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
