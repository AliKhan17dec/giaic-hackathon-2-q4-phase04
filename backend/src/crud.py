from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from .models import Conversation, Message, Task # Added Task
from . import schemas # Added schemas


def create_conversation(session: Session, user_id: UUID) -> Conversation:
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation(session: Session, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
    statement = select(Conversation).where(
        Conversation.id == conversation_id, Conversation.user_id == user_id
    )
    return session.exec(statement).first()


def get_messages_for_conversation(session: Session, conversation_id: UUID) -> List[Message]:
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    return session.exec(statement).all()


def create_message(
    session: Session, conversation_id: UUID, role: str, content: str, tool_calls: Optional[dict] = None
) -> Message:
    message = Message(
        conversation_id=conversation_id, role=role, content=content, tool_calls=tool_calls
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_conversations_for_user(session: Session, user_id: UUID) -> List[Conversation]:
    statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at)
    return session.exec(statement).all()


# --- Task CRUD Operations ---
def create_task(session: Session, owner_id: UUID, task: schemas.TaskCreate) -> Task:
    db_task = Task(**task.dict(), owner_id=owner_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_tasks(session: Session, owner_id: UUID) -> List[Task]:
    return session.exec(select(Task).where(Task.owner_id == owner_id)).all()


def get_single_task(session: Session, task_id: UUID, owner_id: UUID) -> Optional[Task]:
    return session.exec(select(Task).where(Task.id == task_id, Task.owner_id == owner_id)).first()


def update_task(session: Session, task_id: UUID, owner_id: UUID, task_update: schemas.TaskUpdate) -> Optional[Task]:
    db_task = session.exec(select(Task).where(Task.id == task_id, Task.owner_id == owner_id)).first()
    if not db_task:
        return None
    
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: UUID, owner_id: UUID) -> bool:
    db_task = session.exec(select(Task).where(Task.id == task_id, Task.owner_id == owner_id)).first()
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True