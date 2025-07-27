from app.models import Database
import secrets
import os

if __name__ == "__main__":
    db_path = 'database.db'
    absolute_path: str = os.path.abspath(db_path)

    if os.path.exists(absolute_path):
        os.remove(absolute_path)

    db = Database(absolute_path)
    db.create_tables()

    key: str = secrets.token_hex(32)

    if os.path.exists(".env"):
        os.remove(".env")

    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={key}\n")
        f.write(f"DATABASE_PATH={absolute_path}\n")

    print("Database initialized and .env file created.")