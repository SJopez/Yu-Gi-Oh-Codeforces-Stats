from sqlmodel import SQLModel, create_engine, Session
from app.models import User


sqlite_url = 'sqlite:///database/codeforces.db'
engine = create_engine(sqlite_url)

def create_database():

    global engine
    SQLModel.metadata.create_all(engine)

def update_database(users : list[User]):
    session = Session(engine)
    for user in users:
        session.merge(user)

    session.commit()

    session.close()