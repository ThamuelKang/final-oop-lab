from pathlib import Path
from utils.file_helpers import load_json, save_json

DATA_FILE_PATH = Path("data/users.json")

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"name: {self.name} | email: {self.email}"

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        data = load_json(DATA_FILE_PATH)
        return [User(u["name"], u["email"]) for u in data]

    def save_users(self):
        data = [{"name": u.name, "email": u.email} for u in self.users]
        save_json(DATA_FILE_PATH, data)

    def add_user(self, name, email):
        new_user = User(name, email)
        self.users.append(new_user)
        self.save_users()
        print(f"Added user: {new_user}")

    def list_users(self):
        for user in self.users:
            print(user)
