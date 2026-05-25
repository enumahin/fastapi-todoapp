import pytest

from features.todos.todo_dto import TodoRequest
from features.todos import todo_service


@pytest.fixture
def default_todo():
    return TodoRequest(title="Learn FastAPI", description="Learn FastAPI", priority=1, completed=False)

@pytest.fixture()
def get_auth_user(default_user):
    return {'id': default_user.id, 'username': default_user.username, 'email': default_user.email, 'role': default_user.role}

@pytest.fixture
def create_todo(default_todo, db_session, get_auth_user):
    return todo_service.create_todo(get_auth_user, default_todo, db_session)

def test_create_todo(get_auth_user, create_todo):
    todo = create_todo

    assert todo.title == "Learn FastAPI"
    assert todo.description == "Learn FastAPI"
    assert todo.priority == 1
    assert todo.completed == False
    assert todo.owner_id == get_auth_user.get('id')


def test_get_all_todos(create_todo, db_session, get_auth_user):
    # Get all todos
    todos = todo_service.get_all_todos(get_auth_user, db_session)
    assert len(todos) == 1

def test_get_todo(create_todo, db_session, get_auth_user):
    todo = todo_service.get_todo(get_auth_user, create_todo.id, db_session)

    assert todo.title == create_todo.title
    assert todo.description == create_todo.description

def test_update_todo(create_todo, db_session, get_auth_user):
    todo_request = TodoRequest(title="Learn FastAPI Updated", description="Learn FastAPI Updated", priority=1, completed=True)
    updated_todo = todo_service.update_todo(get_auth_user, db_session, todo_request, create_todo.id)

    assert updated_todo.title == "Learn FastAPI Updated"
    assert updated_todo.completed is True

def test_delete_todo(create_todo, get_auth_user, db_session):
    response = todo_service.delete_todo(get_auth_user, db_session, create_todo.id)

    assert response == "Todo deleted successfully"