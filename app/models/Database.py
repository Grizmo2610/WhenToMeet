import sqlite3
from datetime import datetime, timezone
from typing import Any, List, Optional

class Database:
    def __init__(self, db_path: str = "database.db") -> None:
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def execute(self, query: str, params: tuple = ()) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def create_tables(self) -> None:
        self.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                createdAt TIMESTAMP NOT NULL,
                lastLogin TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ownerId INTEGER,
                title TEXT,
                description TEXT,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ownerId) REFERENCES users(id)
            )
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS availabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meetingId INTEGER,
                userId INTEGER,
                date DATE,
                time TIME,
                FOREIGN KEY (meetingId) REFERENCES meetings(id),
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        ''')

    def drop_tables(self) -> None:
        self.execute("DROP TABLE IF EXISTS availabilities")
        self.execute("DROP TABLE IF EXISTS meetings")
        self.execute("DROP TABLE IF EXISTS users")

    def new_user(self, username, password):
        now: datetime = datetime.now(timezone.utc)
        self.execute(
            "INSERT INTO users (username, password, createdAt, lastLogin) VALUES (?, ?, ?, ?)",
            (username, password, now.isoformat(), now.isoformat())
            )

    def find_user(self, key: str, value: str):
        if key == "username":
            return self.fetch_one("SELECT id FROM users WHERE username = ?", (value,))
        elif key == "user_id":
            return self.fetch_one("SELECT id FROM users WHERE id = ", (value, ))
        return None