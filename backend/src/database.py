from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from os import environ as env
from dotenv import load_dotenv
import os

from sqlmodel import Session, SQLModel, create_engine

# Load environment variables from the .env file in the backend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

DATABASE_URL = env.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session