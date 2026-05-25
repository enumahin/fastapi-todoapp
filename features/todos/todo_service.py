from fastapi import HTTPException

from core.auth import user_dependency
from features.todos import todo_dao
from features.todos.todo_dto import TodoRequest
from features.todos.todo_model import Todo



def create_todo(user: user_dependency, todo_request: TodoRequest, db):
    try:
        todo = Todo()
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.completed = todo_request.completed
        todo.owner_id = user.get('id')
        created_todo = todo_dao.create_todo(todo, db)
        return created_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_todos(user: user_dependency, db):
    return todo_dao.get_all_todos(user.get('id'), db)

def get_todo(user, todo_id, db):
    todo = todo_dao.get_todo(user.get('id'), todo_id, db)
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

def update_todo(user, db, todo_request: TodoRequest, todo_id):
    try:
        todo = todo_dao.get_todo(user.get('id'), todo_id, db)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.completed = todo_request.completed
        return todo_dao.update_todo(todo, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_todo(user, db, todo_id):
    try:
        todo = todo_dao.get_todo(user.get('id'), todo_id, db)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo_dao.delete_todo(todo, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))