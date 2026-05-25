import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
try:
    load_dotenv(override=False)
except Exception as e:
    print(e)

def get_database_uri():
    DB_CONN = os.getenv("DB_CONN")
    DB_TYPE = os.getenv("DB_TYPE")

    if DB_CONN:
        return DB_CONN

    if DB_TYPE == "prod":
        return (
            f"{os.getenv('DB_CONNECTOR')}://"
            f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
            f"/{os.getenv('DB_NAME')}"
        )

    return os.getenv("LOCAL_DB_URI", "sqlite:///./todoapp.db")

# Base is a declarative class that will be used to define our tables
Base = declarative_base()

# Global engine and sessionmaker, initialized lazily
_engine = None
_SessionLocal = None

def reset_engine():
    global _engine, _SessionLocal
    _engine = None
    _SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(get_database_uri())
    return _engine

def get_sessionmaker():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

# Create a connection to the database (lazy initialization)
# For backward compatibility, engine is a callable that returns the actual engine
def engine():
    return get_engine()

# This function ensures that the database session is closed after each request
def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

