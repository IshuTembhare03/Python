# core/user_manager.py
import json
from base.user_base import UserBase
from utils import generate_id, get_current_time, read_json, write_json

USER_FILE = "users.json"
TEAM_USER_FILE = "team_users.json"

class UserManager(UserBase):
    def create_user(self, request: str) -> str:
        data = json.loads(request)
        name = data.get("name")
        display_name = data.get("display_name")

        if not name or not display_name:
            raise Exception("Missing fields")

        if len(name) > 64 or len(display_name) > 64:
            raise Exception("Field lengths exceeded")

        users = read_json(USER_FILE)
        if name in [u["name"] for u in users.values()]:
            raise Exception("User already exists")

        user_id = generate_id()
        users[user_id] = {
            "id": user_id,
            "name": name,
            "display_name": display_name,
            "creation_time": get_current_time()
        }
        write_json(USER_FILE, users)
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users = read_json(USER_FILE)
        return json.dumps([
            {
                "name": u["name"],
                "display_name": u["display_name"],
                "creation_time": u["creation_time"]
            } for u in users.values()
        ])

    def describe_user(self, request: str) -> str:
        user_id = json.loads(request)["id"]
        users = read_json(USER_FILE)
        user = users.get(user_id)
        if not user:
            raise Exception("User not found")
        return json.dumps(user)

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data["id"]
        new_data = data["user"]

        users = read_json(USER_FILE)
        if user_id not in users:
            raise Exception("User not found")

        if "name" in new_data and new_data["name"] != users[user_id]["name"]:
            raise Exception("User name cannot be updated")

        if "display_name" in new_data and len(new_data["display_name"]) > 128:
            raise Exception("Display name too long")

        users[user_id]["display_name"] = new_data["display_name"]
        write_json(USER_FILE, users)
        return json.dumps({"message": "User updated"})

    def get_user_teams(self, request: str) -> str:
        user_id = json.loads(request)["id"]
        team_users = read_json(TEAM_USER_FILE)
        teams = read_json("teams.json")
        result = []

        for team_id, user_ids in team_users.items():
            if user_id in user_ids:
                team = teams.get(team_id)
                if team:
                    result.append({
                        "name": team["name"],
                        "description": team["description"],
                        "creation_time": team["creation_time"]
                    })

        return json.dumps(result)
