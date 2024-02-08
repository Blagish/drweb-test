from flask import Flask
from app.config import db_name, file_dir
from app.classes import files_path
import os
import sqlite3

app = Flask(__name__)

with sqlite3.connect(db_name) as conn:
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    owner TEXT
    )
    ''')
    conn.commit()

if not os.path.exists(files_path):
    os.mkdir(files_path)

from app import views
