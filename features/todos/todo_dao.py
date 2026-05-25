from features.todos.todo_model import Todo


def create_todo(todo, db):
    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        db.rollback()
        raise e

def get_all_todos(user_id, db):
    return db.query(Todo).filter(Todo.owner_id == user_id).all()

def get_todo(user_id, todo_id, db):
    return db.query(Todo).where(Todo.id == todo_id, Todo.owner_id == user_id).first()

def update_todo(todo, db):
    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        db.rollback()
        raise e

def delete_todo(todo, db):
    try:
        db.delete(todo)
        db.commit()
        return "Todo deleted successfully"
    except Exception as e:
        db.rollback()
        raise e