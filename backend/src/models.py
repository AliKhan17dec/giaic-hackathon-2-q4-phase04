from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
import json

from sqlmodel import Field, Relationship, SQLModel, JSON # Import JSON


class UUIDModel(SQLModel):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow}
    )


class User(UUIDModel, table=True):
    __tablename__ = "users"
    username: str = Field(index=True, unique=True, max_length=50)
    hashed_password: str = Field(max_length=255)

    tasks: List["Task"] = Relationship(back_populates="owner")
    conversations: List["Conversation"] = Relationship(back_populates="user")


class Conversation(UUIDModel, table=True):
    __tablename__ = "conversations"
    user_id: UUID = Field(foreign_key="users.id", index=True)
    user: User = Relationship(back_populates="conversations") # Added back_populates

    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(UUIDModel, table=True):
    __tablename__ = "messages"
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=50) # "user", "assistant", "tool", "system"
    content: str = Field(nullable=False)
    tool_calls: Optional[dict] = Field(default=None, sa_column=JSON)

    conversation: Conversation = Relationship(back_populates="messages")


class Task(UUIDModel, table=True):
    __tablename__ = "tasks"
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    owner_id: UUID = Field(foreign_key="users.id")

    owner: User = Relationship(back_populates="tasks")