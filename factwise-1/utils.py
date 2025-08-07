# utils.py
import json
import os
import uuid
from datetime import datetime

DB_DIR = "db"
OUT_DIR = "out"

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def generate_id():
    return str(uuid.uuid4())

def get_current_time():
    return datetime.now().isoformat()

def read_json(filename):
    path = os.path.join(DB_DIR, filename)
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def write_json(filename, data):
    path = os.path.join(DB_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def write_txt(filename, content):
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
