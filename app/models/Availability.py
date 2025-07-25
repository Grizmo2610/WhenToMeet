from typing import Any
from .Database import Database

class Availability:
    def __init__(self, db):
        self.db: Database = db

    def add(self, meeting_id: int, user_id: int, date: str, time: str):
        self.db.execute('''
            INSERT INTO availabilities (meetingId, userId, date, time)
            VALUES (?, ?, ?, ?)
        ''', (meeting_id, user_id, date, time))

    def remove(self, meeting_id: int, user_id: int, date: str, time: str):
        self.db.execute('''
            DELETE FROM availabilities
            WHERE meetingId = ? AND userId = ? AND date = ? AND time = ?
        ''', (meeting_id, user_id, date, time))

    def get_by_user(self, user_id: int, meeting_id: int):
        return self.db.fetch_all('''
            SELECT date, time
            FROM availabilities
            WHERE userId = ? AND meetingId = ?
        ''', (user_id, meeting_id))

    def get_by_meeting(self, meeting_id: int):
        return self.db.fetch_all('''
            SELECT userId, date, time
            FROM availabilities
            WHERE meetingId = ?
        ''', (meeting_id,))

    def get_common_slots(self, meeting_id: int):
        return self.db.fetch_all('''
            SELECT date, time, COUNT(*) as votes
            FROM availabilities
            WHERE meetingId = ?
            GROUP BY date, time
            ORDER BY votes DESC
        ''', (meeting_id,))

    def count_votes_for_slot(self, meeting_id: int, date: str, time: str):
        result = self.db.fetch_one('''
            SELECT COUNT(*) as vote_count
            FROM availabilities
            WHERE meetingId = ? AND date = ? AND time = ?
        ''', (meeting_id, date, time))
        return result["vote_count"] if result else 0
