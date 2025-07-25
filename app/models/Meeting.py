from datetime import datetime
from .Database import Database

class Meeting:
    def __init__(self, db):
        self.db = db

    def create(self, owner_id: int, title: str, description: str):
        self.db.execute('''
            INSERT INTO meetings (ownerId, title, description, createdAt)
            VALUES (?, ?, ?, ?)
        ''', (owner_id, title, description, datetime.now()))

    def get_by_id(self, meeting_id: int):
        return self.db.fetch_one('SELECT * FROM meetings WHERE id = ?', (meeting_id,))

    def get_all_by_user(self, user_id: int):
        return self.db.fetch_all('SELECT * FROM meetings WHERE ownerId = ?', (user_id,))

    def delete(self, meeting_id: int):
        self.db.execute('DELETE FROM meetings WHERE id = ?', (meeting_id,))

    def get_participants(self, meeting_id: int):
        return self.db.fetch_all('''
            SELECT DISTINCT users.id, users.username
            FROM availabilities
            JOIN users ON availabilities.userId = users.id
            WHERE meetingId = ?
        ''', (meeting_id,))

    def get_availability_summary(self, meeting_id: int):
        return self.db.fetch_all('''
            SELECT date, time, COUNT(*) as votes
            FROM availabilities
            WHERE meetingId = ?
            GROUP BY date, time
            ORDER BY votes DESC
        ''', (meeting_id,))
