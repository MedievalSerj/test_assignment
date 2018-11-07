from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


def get_scoped_session(db_url):
    return scoped_session(sessionmaker(bind=create_engine(db_url)))
