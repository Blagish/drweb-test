import sqlite3
import os
from app.config import file_dir, db_name


files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_dir)


class File:
    def __init__(self, file_hash):
        self.name = file_hash
        self.dir_path = os.path.join(files_path, self.name[:2])
        self.full_path = os.path.join(self.dir_path, self.name)
        self.exists = False
        if os.path.exists(self.full_path):
            self.exists = True
        
    def save(self, file, owner):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        file.save(self.full_path)
        self._save_db(owner)

    def delete(self, user):
        if self._is_owner_db(user):
            self._delete_db(user)
            os.remove(self.full_path)

    def _save_db(self, owner):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO files (name, owner) VALUES (?, ?)', (self.name, owner))
            conn.commit()
    
    def _delete_db(self, user):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM files WHERE name = ? AND owner = ?', (self.name, user))
            conn.commit()

    def _is_owner_db(self, user):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM files WHERE name = ? AND owner = ?', (self.name, user))
            res = cursor.fetchall()
            conn.commit()
        return len(res) != 0

