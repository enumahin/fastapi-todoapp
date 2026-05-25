import pytest

from features.todos import todo_dao
from features.todos.todo_model import Todo

@pytest.fixture
def default_todo():
    return Todo(title="Learn FastAPI", description="Learn FastAPI", priority=1, completed=False)

@pytest.fixture
def create_todo(default_todo, db_session, default_user):
    default_todo.owner_id = default_user.id
    return todo_dao.create_todo(default_todo, db_session)

def test_create_todo(default_user, create_todo):
    todo = create_todo

    assert todo.title == "Learn FastAPI"
    assert todo.description == "Learn FastAPI"
    assert todo.priority == 1
    assert todo.completed == False
    assert todo.owner_id == default_user.id

def test_get_all_todos(create_todo, db_session, default_user):
    # Get all todos
    todos = todo_dao.get_all_todos(default_user.id, db_session)
    assert len(todos) == 1

def test_get_todo(create_todo, db_session, default_user):
    todo = todo_dao.get_todo(user_id=default_user.id, todo_id=create_todo.id, db=db_session)

    assert todo.title == create_todo.title
    assert todo.description == create_todo.description

def test_update_todo(create_todo, db_session, default_user):
    todo = todo_dao.get_todo(user_id=default_user.id, todo_id=create_todo.id, db=db_session)
    todo.title = "Learn FastAPI Updated"
    todo.completed = True
    updated_todo = todo_dao.update_todo(todo, db_session)

    assert updated_todo.title == "Learn FastAPI Updated"
    assert updated_todo.completed is True

def test_delete_todo(create_todo, db_session):
    response = todo_dao.delete_todo(create_todo, db_session)

    assert response == "Todo deleted successfully"