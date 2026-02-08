from typing import Dict, Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from . import models, crud


class MCPTools:
    def __init__(self, db_session: Session, user_id: UUID):
        self.db_session = db_session
        self.user_id = user_id

    def add_task(self, description: str, title: str = None) -> Dict[str, Any]:
        """Adds a new task for the current user."""
        if not description:
            raise HTTPException(status_code=400, detail="Task description cannot be empty.")
        
        # Use existing create_task logic via crud
        task_create = crud.schemas.TaskCreate(title=title if title else description, description=description) # Assuming schemas is available through crud
        db_task = crud.create_task(self.db_session, self.user_id, task_create) # Assuming crud.create_task handles user_id
        return {"status": "success", "task_id": str(db_task.id), "title": db_task.title, "description": db_task.description}

    def get_tasks(self) -> Dict[str, Any]:
        """Retrieves all tasks for the current user."""
        tasks = crud.get_tasks(self.db_session, self.user_id) # Assuming crud.get_tasks handles user_id
        return {"status": "success", "tasks": [{"id": str(t.id), "title": t.title, "description": t.description, "completed": t.completed} for t in tasks]}

    def update_task_status(self, task_id: str, completed: bool) -> Dict[str, Any]:
        """Updates the completion status of a task."""
        # task_id is expected as a UUID string from tools / openai
        try:
            task_uuid = UUID(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task_id format")

        task = crud.get_single_task(self.db_session, task_uuid, self.user_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")

        task_update = crud.schemas.TaskUpdate(completed=completed)
        updated_task = crud.update_task(self.db_session, task_uuid, self.user_id, task_update)
        return {"status": "success", "task_id": str(updated_task.id), "completed": updated_task.completed}

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Deletes a task by its ID."""
        try:
            task_uuid = UUID(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task_id format")

        deleted = crud.delete_task(self.db_session, task_uuid, self.user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found or not authorized.")
        return {"status": "success", "task_id": str(task_id)}
