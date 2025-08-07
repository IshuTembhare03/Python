# core/team_manager.py
import json
from base.team_base import TeamBase
from utils import generate_id, get_current_time, read_json, write_json

TEAM_FILE = "teams.json"
TEAM_USER_FILE = "team_users.json"
USER_FILE = "users.json"

class TeamManager(TeamBase):
    def create_team(self, request: str) -> str:
        data = json.loads(request)
        name, desc, admin = data["name"], data["description"], data["admin"]

        if len(name) > 64 or len(desc) > 128:
            raise Exception("Name or description too long")

        teams = read_json(TEAM_FILE)
        if name in [t["name"] for t in teams.values()]:
            raise Exception("Team name must be unique")

        team_id = generate_id()
        teams[team_id] = {
            "id": team_id,
            "name": name,
            "description": desc,
            "admin": admin,
            "creation_time": get_current_time()
        }
        write_json(TEAM_FILE, teams)

        team_users = read_json(TEAM_USER_FILE)
        team_users[team_id] = [admin]
        write_json(TEAM_USER_FILE, team_users)

        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams = read_json(TEAM_FILE)
        return json.dumps([v for v in teams.values()])

    def describe_team(self, request: str) -> str:
        team_id = json.loads(request)["id"]
        teams = read_json(TEAM_FILE)
        return json.dumps(teams.get(team_id, {}))

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data["id"]
        new_data = data["team"]

        teams = read_json(TEAM_FILE)
        if team_id not in teams:
            raise Exception("Team not found")

        for team in teams.values():
            if team["name"] == new_data["name"] and team["id"] != team_id:
                raise Exception("Team name must be unique")

        teams[team_id].update(new_data)
        write_json(TEAM_FILE, teams)
        return json.dumps({"message": "Team updated"})

    def add_users_to_team(self, request: str):
        data = json.loads(request)
        team_id, users = data["id"], data["users"]

        team_users = read_json(TEAM_USER_FILE)
        if team_id not in team_users:
            team_users[team_id] = []

        current_users = set(team_users[team_id])
        current_users.update(users)

        if len(current_users) > 50:
            raise Exception("Cannot exceed 50 users per team")

        team_users[team_id] = list(current_users)
        write_json(TEAM_USER_FILE, team_users)

    def remove_users_from_team(self, request: str):
        data = json.loads(request)
        team_id, users = data["id"], data["users"]

        team_users = read_json(TEAM_USER_FILE)
        if team_id in team_users:
            current_users = set(team_users[team_id])
            current_users.difference_update(users)
            team_users[team_id] = list(current_users)
            write_json(TEAM_USER_FILE, team_users)

    def list_team_users(self, request: str):
        team_id = json.loads(request)["id"]
        team_users = read_json(TEAM_USER_FILE)
        users = read_json(USER_FILE)

        result = []
        for user_id in team_users.get(team_id, []):
            if user_id in users:
                result.append({
                    "id": user_id,
                    "name": users[user_id]["name"],
                    "display_name": users[user_id]["display_name"]
                })

        return json.dumps(result)
