from datetime import datetime
from typing import Any
from .Database import Database

class EventManager:
    def __init__(self, user_id: int = None, db: Database = ...):
        self.user_id = user_id
        self.db = db
        self.login_time = datetime.now()
        self.active = True

    def end_session(self):
        self.active = False

    def is_active(self):
        if self.user_id:
            return self.active

    def get_profile(self):
        if self.user_id:
            return self.db.fetch_one('SELECT * FROM users WHERE id = ?', (self.user_id,))

    def get_my_meetings(self):
        if self.user_id:
            return self.db.fetch_all('SELECT * FROM meetings WHERE ownerId = ?', (self.user_id,))

    def get_meeting_participants(self, meeting_id: int):
        return self.db.fetch_all('''
            SELECT DISTINCT users.id, users.username
            FROM availabilities
            JOIN users ON availabilities.userId = users.id
            WHERE meetingId = ?
        ''', (meeting_id,))

    def get_availabilities(self, meeting_id: int):
        return self.db.fetch_all('''
            SELECT date, time
            FROM availabilities
            WHERE meetingId = ? AND userId = ?
        ''', (meeting_id, self.user_id))

    def create_meeting(self, title: str, description: str):
        self.db.execute('''
            INSERT INTO meetings (ownerId, title, description, createdAt)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, title, description, datetime.now()))

    def add_availability(self, meeting_id: int, date: str, time: str):
        self.db.execute('''
            INSERT INTO availabilities (meetingId, userId, date, time)
            VALUES (?, ?, ?, ?)
        ''', (meeting_id, self.user_id, date, time))

    def remove_availability(self, meeting_id: int, date: str, time: str):
        self.db.execute('''
            DELETE FROM availabilities
            WHERE meetingId = ? AND userId = ? AND date = ? AND time = ?
        ''', (meeting_id, self.user_id, date, time))

    def update_profile(self, **fields):
        set_clause = ', '.join(f"{k}=?" for k in fields)
        values = list(fields.values())
        values.append(self.user_id)
        self.db.execute(f'''
            UPDATE users SET {set_clause} WHERE id = ?
        ''', tuple(values))
