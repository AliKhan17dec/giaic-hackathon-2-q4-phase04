import pytest
from unittest.mock import MagicMock
from backend.src.agent import AIAgent # Assuming AIAgent is in backend.src.agent
# from backend.src.mcp_tools import add_task, get_tasks, update_task, delete_task # Assuming these will be implemented


# Mock OpenAI client to avoid actual API calls during testing
@pytest.fixture
def mock_openai_client():
    mock_client = MagicMock()
    # Mocking a simple AI response without tool calls for initial tests
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Mocked AI response"))]
    )
    return mock_client


@pytest.fixture
def ai_agent(mock_openai_client):
    agent = AIAgent(openai_api_key="sk-mock-key") # Use a mock key
    agent.client = mock_openai_client # Inject mock client
    return agent


def test_ai_agent_initialization(ai_agent):
    assert ai_agent.model == "gpt-4"
    assert ai_agent.tools == []
    assert ai_agent.messages == []


def test_ai_agent_add_message(ai_agent):
    ai_agent.add_message("user", "Hello")
    assert {"role": "user", "content": "Hello"} in ai_agent.messages


def test_ai_agent_run_no_tool_call(ai_agent):
    ai_agent.add_message("user", "What is the weather?")
    response = ai_agent.run()
    assert response == "Mocked AI response"
    ai_agent.client.chat.completions.create.assert_called_once()


# Placeholder for tool selection logic test (T020) - to be expanded
def test_ai_agent_tool_selection_placeholder(ai_agent):
    # This test will involve:
    # 1. Defining a mock tool and adding it to agent.tools
    # 2. Mocking OpenAI response to include tool_calls
    # 3. Running the agent and asserting that the tool is called with correct arguments
    pass
