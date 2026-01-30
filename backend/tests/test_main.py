from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from backend.src.main import app # Corrected import
from backend.src.database import get_session # Corrected import
import pytest

# Database setup for testing
# Use an in-memory SQLite database for testing
testing_engine = create_engine("sqlite:///test.db")


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(testing_engine)
    with Session(testing_engine) as session:
        yield session
    SQLModel.metadata.drop_all(testing_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_root_reads_hello_world(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


# Placeholder for chat endpoint integration test
def test_chat_endpoint_integration_placeholder(client: TestClient):
    # This test will be implemented as part of T018, once the chat endpoint is ready.
    # It will involve:
    # 1. Creating a test user and obtaining a JWT token.
    # 2. Making a POST request to /api/{user_id}/chat.
    # 3. Asserting the response structure and content.
    pass


# Placeholder for chat endpoint integration test with MCP tools (T021)
def test_chat_endpoint_mcp_tools_integration_placeholder(client: TestClient):
    # This test will be implemented as part of T021, once MCP tools and agent integration are ready.
    # It will involve:
    # 1. Creating a test user and obtaining a JWT token.
    # 2. Mocking MCP tool responses.
    # 3. Making a POST request to /api/{user_id}/chat with a message that triggers a tool.
    # 4. Asserting the AI response and that the tool was invoked.
    pass


# Integration test for chat endpoint to ensure history persistence (T027)
def test_chat_history_persistence(client: TestClient, session: Session):
    # Create a test user directly in the database
    test_user_id = UUID("00000000-0000-0000-0000-000000000001")
    hashed_password = auth.Giga.get_password_hash("testpassword")
    test_user = models.User(id=test_user_id, username="testuser_history", hashed_password=hashed_password)
    session.add(test_user)
    session.commit()
    session.refresh(test_user)

    # Obtain a JWT token for the test user
    token_data = {"sub": test_user.username, "user_id": test_user.id}
    access_token = auth.create_access_token(token_data)
    headers = {"Authorization": f"Bearer {access_token}"}

    # First message to start a conversation
    chat_request_1 = schemas.ChatRequest(message="Hello AI")
    response_1 = client.post(f"/api/{test_user_id}/chat", json=chat_request_1.dict(), headers=headers)
    assert response_1.status_code == 200
    response_data_1 = response_1.json()
    assert response_data_1["ai_response"] is not None
    assert response_data_1["conversation_id"] is not None
    initial_conversation_id = UUID(response_data_1["conversation_id"])

    # Send another message in the same conversation
    chat_request_2 = schemas.ChatRequest(message="How are you?", conversation_id=initial_conversation_id)
    response_2 = client.post(f"/api/{test_user_id}/chat", json=chat_request_2.dict(), headers=headers)
    assert response_2.status_code == 200
    response_data_2 = response_2.json()
    assert response_data_2["ai_response"] is not None
    assert UUID(response_data_2["conversation_id"]) == initial_conversation_id

    # Verify conversation and messages in the database
    retrieved_conversation = crud.get_conversation(session, initial_conversation_id, test_user_id)
    assert retrieved_conversation is not None
    assert retrieved_conversation.id == initial_conversation_id
    assert retrieved_conversation.user_id == test_user_id

    retrieved_messages = crud.get_messages_for_conversation(session, initial_conversation_id)
    assert len(retrieved_messages) == 4 # 2 user messages + 2 AI responses
    assert retrieved_messages[0].content == "Hello AI"
    assert retrieved_messages[1].role == "assistant"
    assert retrieved_messages[2].content == "How are you?"
    assert retrieved_messages[3].role == "assistant"


