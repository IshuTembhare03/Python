# Team Project Planner Tool

## Overview
This tool manages teams, users, boards, and tasks using clean APIs. It uses file-based persistence via JSON.

## Structure
- `core/` – Contains concrete logic for APIs
- `base/` – Contains abstract base classes
- `db/` – Stores persistent JSON files
- `out/` – Board exports in text format

## Features
- Create, update, describe users
- Create, update, list teams
- Create task boards and tasks
- Export boards to .txt files

## How to Run
```bash
python main.py
