import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path="bot_data.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    authorized INTEGER DEFAULT 0,
                    admin INTEGER DEFAULT 0,
                    plan TEXT,
                    expiry TEXT
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS log_channels (
                    bot_username TEXT PRIMARY KEY,
                    channel_id INTEGER
                )
            """)
            conn.commit()

    def is_user_authorized(self, user_id, bot_username=None):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT authorized FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            return row is not None and row[0] == 1

    def is_admin(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT admin FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            return row is not None and row[0] == 1

    def add_user(self, user_id, username=None):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO users (user_id, username, authorized, admin) VALUES (?, ?, 1, 0)", (user_id, username))
            conn.commit()

    def remove_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

    def list_users(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id, username FROM users WHERE authorized = 1")
            return c.fetchall()

    def set_log_channel(self, bot_username, channel_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO log_channels (bot_username, channel_id) VALUES (?, ?)", (bot_username, channel_id))
            conn.commit()
            return True

    def get_log_channel(self, bot_username):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT channel_id FROM log_channels WHERE bot_username = ?", (bot_username,))
            row = c.fetchone()
            return row[0] if row else None

db = Database()
