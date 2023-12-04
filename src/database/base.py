from sqlalchemy import create_engine, Column, INT
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.validation.settings import settings


class Base(DeclarativeBase):
    engine = create_engine(url=settings.DB_URL.unicode_string())
    session = sessionmaker(bind=engine)

    id = Column(INT, primary_key=True)


