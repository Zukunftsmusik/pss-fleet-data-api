from src.database import db

SQLITE_FILE_NAME = "test.sqlite"
DATABASE_URL = f"sqlite:///app/tests/{SQLITE_FILE_NAME}"


def create_sqlite():
    db.set_up_db_engine(DATABASE_URL)
    db.initialize_db(db.ENGINE, "examples")
