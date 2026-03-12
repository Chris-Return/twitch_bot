from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///bot.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

with engine.connect() as conn:
    conn.exec_driver_sql("PRAGMA journal_mode=WAL;")

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass