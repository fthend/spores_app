from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Включение поддержки внешних ключей для SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine)

def dispose_engine():
    engine.dispose()

@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()