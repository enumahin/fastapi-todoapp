from typing import Annotated

from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from starlette import status

from core.auth import user_dependency
from database.dbconfig import get_db

from features.todos import todo_service
from features.todos.todo_dto import TodoRequest

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

@router.get("/")
async def get_all_todos(user: user_dependency, db: db_dependency):
    return todo_service.get_all_todos(user, db)

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    return todo_service.get_todo(user, todo_id, db)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, todo_request: TodoRequest, db: db_dependency):
    return todo_service.create_todo(user, todo_request, db)


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    return todo_service.update_todo(user, db, todo_request, todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    return todo_service.delete_todo(user, db, todo_id)
