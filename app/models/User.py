from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .Database import Database

class User:
    def __init__(self, db):
        self.db: Database = db

    def register(self, email: str, password: str, username: str) -> dict[str, int | str]:
        if self.db.find_user("email", email):
            return {'status': 409, 'message': 'Email already exists'}
        hashed = generate_password_hash(password)
        self.db.new_user(email, hashed, username)
        return {'status': 200, 'message': 'Registration successful'}

    def login(self,  email: str, password: str) -> dict | None:
        user = self.db.fetch_one(
            "SELECT id, email, password, username, createdAt, lastLogin FROM users WHERE email = ?",
            (email,)
        )
        if user:
            if check_password_hash(user[2], password):
                self.update_last_login(user[0])
                return {
                    "id": user[0],
                    "name": user[1],
                    "username": user[2],
                    "created_at": user[4],
                    "last_login": user[5],
                    "status": 200,
                    "message": "Succesfully" ,
                }
        return {
            "status": 401,
            "message": "Invalid email or password"
            }

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

