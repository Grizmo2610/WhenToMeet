from ultils.Database import Database
import secrets
import os

if __name__ == "__main__":
    db_path = 'database.db'
    absolute_path = os.path.abspath(db_path)
    db = Database(absolute_path)
    db.create_tables()
    key = secrets.token_hex(32)
    with open("private/.env", "w") as f:
        f.write(f"SECRET_KEY={key}\n")
        f.write(f'DATABASE_PATH={absolute_path}\n')
    print("Database initialized and .env file created.")