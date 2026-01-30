from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, SQLModel
from uuid import UUID
from .database import create_db_and_tables, get_session
from . import models, schemas, auth, crud
from .agent import AIAgent
import logging
from os import environ as env
import json # Added import

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow requests from the frontend dev server during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # change to your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unexpected error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true",
            "Vary": "Origin",
        },
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/api/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_user = db.exec(select(models.User).where(models.User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.Giga.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/login")
def login(form_data: schemas.UserLogin, db: Session = Depends(get_session)):
    user = db.exec(select(models.User).where(models.User.username == form_data.username)).first()
    if not user or not auth.Giga.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/{user_id}/tasks", response_model=schemas.Task)
def create_task(
    user_id: UUID,
    task: schemas.TaskCreate,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create tasks for this user")
    
    db_task = crud.create_task(db, user_id, task)
    return db_task

@app.get("/api/{user_id}/tasks", response_model=list[schemas.Task])
def get_tasks(
    user_id: UUID,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view tasks for this user")
    
    tasks = crud.get_tasks(db, user_id)
    return tasks

@app.get("/api/{user_id}/tasks/{id}", response_model=schemas.Task)
def get_single_task(
    user_id: UUID,
    id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this task")
    
    task = crud.get_single_task(db, id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/{user_id}/tasks/{id}", response_model=schemas.Task)
def update_task(
    user_id: UUID,
    id: int,
    task: schemas.TaskUpdate,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update tasks for this user")
    
    updated_task = crud.update_task(db, id, user_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.patch("/api/{user_id}/tasks/{id}/complete", response_model=schemas.Task)
def complete_task(
    user_id: UUID,
    id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to complete tasks for this user")
    
    task_update = schemas.TaskUpdate(completed=True)
    updated_task = crud.update_task(db, id, user_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/api/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: UUID,
    id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete tasks for this user")
    
    deleted = crud.delete_task(db, id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return

@app.get("/api/{user_id}/conversations", response_model=List[schemas.Conversation])
def get_user_conversations(
    user_id: UUID,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view conversations for this user")
    
    conversations = crud.get_conversations_for_user(db, user_id)
    return conversations

@app.get("/api/{user_id}/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def get_conversation_messages(
    user_id: UUID,
    conversation_id: UUID,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view messages for this user")
    
    conversation = crud.get_conversation(db, conversation_id, user_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    messages = crud.get_messages_for_conversation(db, conversation_id)
    return messages


@app.post("/api/{user_id}/chat", response_model=schemas.ChatResponse)
async def chat_endpoint(
    user_id: UUID,
    chat_request: schemas.ChatRequest,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to chat for this user")

    conversation_id = chat_request.conversation_id
    conversation = None

    if conversation_id:
        conversation = crud.get_conversation(db, conversation_id, user_id)
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    else:
        conversation = crud.create_conversation(db, user_id)
        conversation_id = conversation.id

    # Add user message to conversation
    crud.create_message(db, conversation_id, "user", chat_request.message)

    # Initialize AI agent
    openai_api_key = env.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="OPENAI_API_KEY not configured")
    
    agent = AIAgent(openai_api_key=openai_api_key)
    
    # Initialize MCPTools with db session and user_id
    mcp_tools = MCPTools(db_session=db, user_id=user_id)

    # Register MCP tools with the AI agent
    agent.register_tool(
        tool_name="add_task",
        tool_function=mcp_tools.add_task,
        tool_openai_definition={
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Adds a new task for the current user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string", "description": "The description of the task."},
                        "title": {"type": "string", "description": "The title of the task."},
                    },
                    "required": ["description"],
                },
            },
        },
    )
    agent.register_tool(
        tool_name="get_tasks",
        tool_function=mcp_tools.get_tasks,
        tool_openai_definition={
            "type": "function",
            "function": {
                "name": "get_tasks",
                "description": "Retrieves all tasks for the current user.",
                "parameters": {"type": "object", "properties": {}},
            },
        },
    )
    agent.register_tool(
        tool_name="update_task_status",
        tool_function=mcp_tools.update_task_status,
        tool_openai_definition={
            "type": "function",
            "function": {
                "name": "update_task_status",
                "description": "Updates the completion status of a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to update."},
                        "completed": {"type": "boolean", "description": "The new completion status (true/false)."},
                    },
                    "required": ["task_id", "completed"],
                },
            },
        },
    )
    agent.register_tool(
        tool_name="delete_task",
        tool_function=mcp_tools.delete_task,
        tool_openai_definition={
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Deletes a task by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to delete."},
                    },
                    "required": ["task_id"],
                },
            },
        },
    )


    agent.add_message("user", chat_request.message)
    
    ai_response_content = agent.run()

    # Extract tool calls from agent.messages if any, assuming the last message is the assistant's final response
    tool_calls_response = []
    last_assistant_message = next((m for m in reversed(agent.messages) if m["role"] == "assistant"), None)
    if last_assistant_message and last_assistant_message.tool_calls:
        for tool_call in last_assistant_message.tool_calls:
            tool_calls_response.append(
                schemas.ToolCall(
                    tool_name=tool_call.function.name,
                    tool_args=json.loads(tool_call.function.arguments)
                )
            )

    # Add AI response to conversation
    crud.create_message(db, conversation_id, "assistant", ai_response_content, tool_calls=tool_calls_response)


    return schemas.ChatResponse(
        ai_response=ai_response_content,
        conversation_id=conversation_id,
        tool_calls=tool_calls_response
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}