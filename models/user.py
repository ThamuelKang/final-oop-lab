import json
from pathlib import Path

# Stores path as object using Path()
DATA_FILE_PATH = Path("data/users.json")


# User class
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"name: {self.name} and email: {self.email}"


# User Management helper class
class UserManager:
    def __init__(self):
        self.users = self.load_users()

    # Load users
    def load_users(self):
        try:
            with open(DATA_FILE_PATH, "r") as file:

                # Converts it to JSON -> Python Objects
                data = json.load(file)

                # Converts Python Objects and creates Users()
                users = []
                for u in data:
                    name = u["name"]
                    email = u["email"]
                    user = User(name, email)
                    users.append(user)
                return users
        except FileNotFoundError:
            print("File not found, returning an empty list")
            return []
        except json.JSONDecodeError:
            print("JSON format is bad, returning an empty list")
            return []

    # Saving logic
    def save_users(self):
        saved_data = []

        for user in self.users:
            user_dictionary = {"name": user.name, "email": user.email}
            saved_data.append(user_dictionary)

        # Must overwrite and need JSON formatting!
        with open(DATA_FILE_PATH, "w") as file:
            json.dump(saved_data, file, indent=2)

    # Add user functionality
    def add_user(self, name, email):
        new_user = User(name, email)
        self.users.append(new_user)
        self.save_users()
        print(f"{new_user.name} ({new_user.email}) has been added")

    # Lists all users
    def list_users(self):
        for user in self.users:
            print(user)
