from sqlmodel import SQLModel, create_engine, Session
from sqlmodel import select, func
from app.models import User

sqlite_url = 'sqlite:///database/codeforces.db'
engine = create_engine(sqlite_url)

def create_database():

    global engine
    SQLModel.metadata.create_all(engine)

async def update_database(users : list[User]):

    session = Session(engine)
    for user in users:
        session.merge(user)

    session.commit()

    session.close()

async def get_user_info_db(handle: str) -> User | None:
    
    with Session(engine) as session:
        statement = select(User).where(func.lower(User.handle) == handle.lower())
        return session.exec(statement).first()
