import pytest

@pytest.fixture
def default_todo():
    return {
            'title': "Learn FastAPI",
            'description': "Learn FastAPI",
            'priority': 1,
            'completed': False
    }


@pytest.fixture
def create_todo(client, default_todo, db_session, get_auth_user):
    response = client.post("/todos", json=default_todo,
                           headers={"Authorization": f"Bearer {get_auth_user.get('access_token')}"})
    return response.json()

def test_create_todo(get_auth_user, create_todo):
    todo = create_todo

    assert todo.get('title') == "Learn FastAPI"
    assert todo.get('description') == "Learn FastAPI"
    assert todo.get('priority') == 1
    assert todo.get('completed') == False
    assert todo.get('owner_id') == get_auth_user.get('id')


def test_get_all_todos(client, create_todo, get_auth_user):
    # Get all todos
    response = client.get("/todos",
                       headers={"Authorization": f"Bearer {get_auth_user.get('access_token')}"})
    todos = response.json()
    assert len(todos) == 1

def test_get_todo(client, create_todo, get_auth_user):
    response = client.get(f"/todos/{create_todo.get('id')}",
                      headers={"Authorization": f"Bearer {get_auth_user.get('access_token')}"}
                    )
    todo = response.json()
    assert todo.get('title') == create_todo.get('title')
    assert todo.get('description') == create_todo.get('description')

def test_update_todo(client, create_todo, get_auth_user):
    todo_request = {'title': "Learn FastAPI Updated",
                    'description': "Learn FastAPI Updated",
                    'priority': 1,
                    'completed': True
                    }
    response = client.put(f"/todos/{create_todo.get('id')}", json=todo_request,
                              headers={"Authorization": f"Bearer {get_auth_user.get('access_token')}"}
                              )
    updated_todo = response.json()
    assert updated_todo.get('title') == "Learn FastAPI Updated"
    assert updated_todo.get('completed') is True

def test_delete_todo(client, create_todo, get_auth_user):
    response = client.delete(f"/todos/{create_todo.get('id')}",
                             headers={"Authorization": f"Bearer {get_auth_user.get('access_token')}"})

    assert response.json() == "Todo deleted successfully"