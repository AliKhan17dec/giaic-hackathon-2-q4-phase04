from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from .database import create_db_and_tables, get_session
from . import models, schemas, auth
import logging

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
    user_id: int,
    task: schemas.TaskCreate,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create tasks for this user")
    
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/api/{user_id}/tasks", response_model=list[schemas.Task])
def get_tasks(
    user_id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view tasks for this user")
    
    tasks = db.exec(select(models.Task).where(models.Task.owner_id == user_id)).all()
    return tasks

@app.get("/api/{user_id}/tasks/{id}", response_model=schemas.Task)
def get_single_task(
    user_id: int,
    id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this task")
    
    task = db.exec(select(models.Task).where(models.Task.id == id, models.Task.owner_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/{user_id}/tasks/{id}", response_model=schemas.Task)
def update_task(
    user_id: int,
    id: int,
    task: schemas.TaskUpdate,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update tasks for this user")
    
    db_task = db.exec(select(models.Task).where(models.Task.id == id, models.Task.owner_id == user_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.patch("/api/{user_id}/tasks/{id}/complete", response_model=schemas.Task)
def complete_task(
    user_id: int,
    id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to complete tasks for this user")
    
    task = db.exec(select(models.Task).where(models.Task.id == id, models.Task.owner_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/api/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    id: int,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_session),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete tasks for this user")
    
    task = db.exec(select(models.Task).where(models.Task.id == id, models.Task.owner_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return

@app.get("/")
def read_root():
    return {"Hello": "World"}
