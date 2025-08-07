# main.py

import json  # ✅ Missing import added here
from core.user_manager import UserManager
from core.team_manager import TeamManager
from core.board_manager import BoardManager
from utils import get_current_time

# Instances
user_api = UserManager()
team_api = TeamManager()
board_api = BoardManager()

# Create user
user = {"name": "john_doe", "display_name": "John"}
user_res = user_api.create_user(json.dumps(user))
user_id = json.loads(user_res)["id"]

# Create team
team = {
    "name": "Alpha",
    "description": "Alpha Team Project",
    "admin": user_id
}
team_res = team_api.create_team(json.dumps(team))
team_id = json.loads(team_res)["id"]

# Create board
board = {
    "name": "Sprint 1",
    "description": "First sprint",
    "team_id": team_id,
    "creation_time": get_current_time()
}
board_res = board_api.create_board(json.dumps(board))
board_id = json.loads(board_res)["id"]

# Add task
task = {
    "title": "Setup Repo",
    "description": "Initialize GitHub repo",
    "user_id": user_id,
    "board_id": board_id,
    "creation_time": get_current_time()
}
task_res = board_api.add_task(json.dumps(task))
task_id = json.loads(task_res)["id"]

# Export board
export = board_api.export_board(json.dumps({"id": board_id}))
print("Exported:", export)
