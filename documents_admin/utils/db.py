from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def get_scoped_session(db_url):
    return scoped_session(sessionmaker(bind=create_engine(db_url)))
