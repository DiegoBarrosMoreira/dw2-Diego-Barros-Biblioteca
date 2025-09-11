import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Livro

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db.sqlite3")
DB_URI = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
	Base.metadata.create_all(bind=engine)
