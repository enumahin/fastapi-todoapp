
from fastapi import FastAPI
from database.dbconfig import engine, Base
from core.auth import auth_router
from core.auth.user import user_router
from features import todos

app = FastAPI()

# Create a database and tables using SQLAlchemy engine
Base.metadata.create_all(bind=engine())

@app.get("/healthy")
def health():
    return {"status": "healthy"}

# Add the auth router we created to app
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(todos.todo_router.router)



