import pytest
from uuid import UUID, uuid4

from sqlmodel import Session, SQLModel, create_engine

from backend.src import crud, models, schemas # Assuming these modules are available


# Database setup for testing
# Use an in-memory SQLite database for testing
testing_engine = create_engine("sqlite:///test.db")


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(testing_engine)
    with Session(testing_engine) as session:
        yield session
    SQLModel.metadata.drop_all(testing_engine)


@pytest.fixture
def test_user_id() -> UUID:
    return uuid4()


@pytest.fixture
def create_test_conversation(session: Session, test_user_id: UUID) -> models.Conversation:
    conversation = crud.create_conversation(session, test_user_id)
    return conversation


def test_create_conversation(session: Session, test_user_id: UUID):
    conversation = crud.create_conversation(session, test_user_id)
    assert conversation.id is not None
    assert conversation.user_id == test_user_id
    assert conversation.created_at is not None
    assert conversation.updated_at is not None


def test_get_conversation(session: Session, create_test_conversation: models.Conversation, test_user_id: UUID):
    retrieved_conversation = crud.get_conversation(session, create_test_conversation.id, test_user_id)
    assert retrieved_conversation == create_test_conversation


def test_get_conversation_not_found(session: Session, test_user_id: UUID):
    non_existent_id = uuid4()
    retrieved_conversation = crud.get_conversation(session, non_existent_id, test_user_id)
    assert retrieved_conversation is None


def test_create_message(session: Session, create_test_conversation: models.Conversation):
    message = crud.create_message(session, create_test_conversation.id, "user", "Hello AI")
    assert message.id is not None
    assert message.conversation_id == create_test_conversation.id
    assert message.role == "user"
    assert message.content == "Hello AI"
    assert message.tool_calls is None


def test_create_message_with_tool_calls(session: Session, create_test_conversation: models.Conversation):
    tool_calls_data = [{"tool_name": "add_task", "tool_args": {"description": "buy milk"}}]
    message = crud.create_message(session, create_test_conversation.id, "assistant", "Okay", tool_calls_data)
    assert message.tool_calls == tool_calls_data


def test_get_messages_for_conversation(session: Session, create_test_conversation: models.Conversation):
    crud.create_message(session, create_test_conversation.id, "user", "Message 1")
    crud.create_message(session, create_test_conversation.id, "assistant", "Response 1")
    messages = crud.get_messages_for_conversation(session, create_test_conversation.id)
    assert len(messages) == 2
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Response 1"


# --- Task CRUD Tests (from crud.py) ---
@pytest.fixture
def create_test_task(session: Session, test_user_id: UUID) -> models.Task:
    task_create = schemas.TaskCreate(title="Test Task", description="Description for test task")
    task = crud.create_task(session, test_user_id, task_create)
    return task


def test_crud_create_task(session: Session, test_user_id: UUID):
    task_create = schemas.TaskCreate(title="New Task", description="New task description")
    task = crud.create_task(session, test_user_id, task_create)
    assert task.id is not None
    assert task.owner_id == test_user_id
    assert task.title == "New Task"
    assert task.description == "New task description"
    assert task.completed is False


def test_crud_get_tasks(session: Session, test_user_id: UUID, create_test_task: models.Task):
    tasks = crud.get_tasks(session, test_user_id)
    assert len(tasks) == 1
    assert tasks[0] == create_test_task


def test_crud_get_single_task(session: Session, test_user_id: UUID, create_test_task: models.Task):
    task = crud.get_single_task(session, create_test_task.id, test_user_id)
    assert task == create_test_task


def test_crud_get_single_task_not_found(session: Session, test_user_id: UUID):
    task = crud.get_single_task(session, 999, test_user_id) # Assuming ID is int
    assert task is None


def test_crud_update_task(session: Session, test_user_id: UUID, create_test_task: models.Task):
    task_update = schemas.TaskUpdate(completed=True)
    updated_task = crud.update_task(session, create_test_task.id, test_user_id, task_update)
    assert updated_task.completed is True


def test_crud_delete_task(session: Session, test_user_id: UUID, create_test_task: models.Task):
    deleted = crud.delete_task(session, create_test_task.id, test_user_id)
    assert deleted is True
    assert crud.get_single_task(session, create_test_task.id, test_user_id) is None