from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String,create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

db_url = "sqlite:///./app.db"
engine = create_engine(db_url, echo=True)

class Base(DeclarativeBase):
    pass

class Task(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]

    __tablename__ = "tasks"


MySession = sessionmaker(bind=engine)


def get_session() -> Session:
    return MySession()
