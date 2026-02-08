from pydantic import BaseModel, validator
from typing import Optional, List, Union
from uuid import UUID # Added UUID
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: UUID # Changed to UUID
    username: str

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Task(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    completed: bool
    owner_id: UUID # Changed to UUID

    class Config:
        orm_mode = True

# New Chat Schemas
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class ToolCall(BaseModel):
    tool_name: str
    tool_args: dict

class Message(BaseModel): # New Message Schema
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    tool_calls: Optional[Union[dict, List]] = None
    created_at: datetime
    updated_at: datetime

    @validator('tool_calls', pre=True)
    def normalize_tool_calls(cls, v):
        # Convert empty list to None for consistency
        if v == [] or v == {}:
            return None
        return v

    class Config:
        orm_mode = True


class Conversation(BaseModel): # New Conversation Schema
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = [] # Include messages to eager load

    class Config:
        orm_mode = True


class ChatResponse(BaseModel):
    ai_response: str
    conversation_id: UUID
    tool_calls: List[ToolCall] = []