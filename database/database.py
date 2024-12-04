import sqlite3
import json

DB_PATH = "database/users.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                page INTEGER DEFAULT 1,
                bookmarks TEXT DEFAULT '[]'
            )
        """)
        conn.commit()

def get_user_data(user_id: int) -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT page, bookmarks FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            page, bookmarks_json = result
            return {
                'page': page,
                'bookmarks': set(json.loads(bookmarks_json))
            }
        else:
            add_user(user_id)
            return {'page': 1, 'bookmarks': set()}

def add_user(user_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

def update_user_page(user_id: int, page: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET page = ? WHERE user_id = ?", (page, user_id))
        conn.commit()

def update_user_bookmarks(user_id: int, bookmarks: set):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        bookmarks_json = json.dumps(list(bookmarks))
        cursor.execute("UPDATE users SET bookmarks = ? WHERE user_id = ?", (bookmarks_json, user_id))
        conn.commit()

init_db()