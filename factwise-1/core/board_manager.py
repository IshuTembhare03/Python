# core/board_manager.py
import json
from base.project_board_base import ProjectBoardBase
from utils import generate_id, get_current_time, read_json, write_json, write_txt

BOARD_FILE = "boards.json"
TASK_FILE = "tasks.json"

class BoardManager(ProjectBoardBase):
    def create_board(self, request: str):
        data = json.loads(request)
        name = data["name"]
        description = data["description"]
        team_id = data["team_id"]
        creation_time = data["creation_time"]

        if len(name) > 64 or len(description) > 128:
            raise Exception("Board name or description too long")

        boards = read_json(BOARD_FILE)
        for b in boards.values():
            if b["name"] == name and b["team_id"] == team_id:
                raise Exception("Board name must be unique per team")

        board_id = generate_id()
        boards[board_id] = {
            "id": board_id,
            "name": name,
            "description": description,
            "team_id": team_id,
            "creation_time": creation_time,
            "status": "OPEN"
        }
        write_json(BOARD_FILE, boards)
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        board_id = json.loads(request)["id"]
        boards = read_json(BOARD_FILE)
        if board_id not in boards:
            raise Exception("Board not found")

        board = boards[board_id]
        if board["status"] != "OPEN":
            raise Exception("Board is not open")

        tasks = read_json(TASK_FILE)
        board_tasks = [t for t in tasks.values() if t["board_id"] == board_id]
        if any(t["status"] != "COMPLETE" for t in board_tasks):
            raise Exception("All tasks must be COMPLETE before closing board")

        board["status"] = "CLOSED"
        board["end_time"] = get_current_time()
        boards[board_id] = board
        write_json(BOARD_FILE, boards)
        return json.dumps({"message": "Board closed"})

    def add_task(self, request: str) -> str:
        data = json.loads(request)
        title = data["title"]
        description = data["description"]
        user_id = data["user_id"]
        creation_time = data["creation_time"]
        board_id = data["board_id"]

        if len(title) > 64 or len(description) > 128:
            raise Exception("Title or description too long")

        boards = read_json(BOARD_FILE)
        if board_id not in boards:
            raise Exception("Board does not exist")

        if boards[board_id]["status"] != "OPEN":
            raise Exception("Board is not open")

        tasks = read_json(TASK_FILE)
        if any(t["title"] == title and t["board_id"] == board_id for t in tasks.values()):
            raise Exception("Task title must be unique for board")

        task_id = generate_id()
        tasks[task_id] = {
            "id": task_id,
            "title": title,
            "description": description,
            "user_id": user_id,
            "board_id": board_id,
            "creation_time": creation_time,
            "status": "OPEN"
        }
        write_json(TASK_FILE, tasks)
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str):
        data = json.loads(request)
        task_id = data["id"]
        new_status = data["status"]

        tasks = read_json(TASK_FILE)
        if task_id not in tasks:
            raise Exception("Task not found")

        if new_status not in ["OPEN", "IN_PROGRESS", "COMPLETE"]:
            raise Exception("Invalid status")

        tasks[task_id]["status"] = new_status
        write_json(TASK_FILE, tasks)
        return json.dumps({"message": "Status updated"})

    def list_boards(self, request: str) -> str:
        team_id = json.loads(request)["id"]
        boards = read_json(BOARD_FILE)
        open_boards = [
            {"id": b["id"], "name": b["name"]}
            for b in boards.values()
            if b["team_id"] == team_id and b["status"] == "OPEN"
        ]
        return json.dumps(open_boards)

    def export_board(self, request: str) -> str:
        board_id = json.loads(request)["id"]
        boards = read_json(BOARD_FILE)
        tasks = read_json(TASK_FILE)

        if board_id not in boards:
            raise Exception("Board not found")

        board = boards[board_id]
        board_tasks = [
            t for t in tasks.values() if t["board_id"] == board_id
        ]

        content = f"Board: {board['name']}\nDescription: {board['description']}\nStatus: {board['status']}\n"
        content += f"Created: {board['creation_time']}\n\nTasks:\n"
        for task in board_tasks:
            content += f"- {task['title']} [{task['status']}]\n  Assigned to: {task['user_id']}\n  Description: {task['description']}\n\n"

        filename = f"{board['name'].replace(' ', '_')}_export.txt"
        write_txt(filename, content)
        return json.dumps({"out_file": filename})
