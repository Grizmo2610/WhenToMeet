from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .Database import Database

class User:
    def __init__(self, db):
        self.db: Database = db
        
    def register(self, username: str, password: str) -> bool:
        if self.db.find_user("username", username):
            return False
        hashed = generate_password_hash(password)
        self.db.new_user(username, hashed)
        return True

    def login(self, username: str, password: str) -> dict | None:
        user = self.db.fetch_one(
            "SELECT id, username, password, createdAt, lastLogin FROM users WHERE username = ?",
            (username,)
        )
        if user and check_password_hash(user[2], password):
            self.update_last_login(user[0])
            return {
                "id": user[0],
                "username": user[1],
                "created_at": user[3],
                "last_login": user[4]
            }
        return None

    def update_last_login(self, user_id: int):
        now = datetime.now().isoformat()
        self.db.execute("UPDATE users SET lastLogin = ? WHERE id = ?", (now, user_id))

    def is_inactive(self, user_id: int, threshold_days: int = 30) -> bool:
        row = self.db.fetch_one("SELECT lastLogin FROM users WHERE id = ?", (user_id,))
        if not row:
            return False
        last_login = datetime.fromisoformat(row[0])
        return datetime.now() - last_login > timedelta(days=threshold_days)

    def delete_if_inactive(self, user_id: int, threshold_days: int = 30):
        if self.is_inactive(user_id, threshold_days):
            self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.db.execute("DELETE FROM meetings WHERE ownerId = ?", (user_id,))
            self.db.execute("DELETE FROM availabilities WHERE userId = ?", (user_id,))

