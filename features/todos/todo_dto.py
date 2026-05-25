from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3, max_length=255)
    priority: int = Field(ge=1, le=5)
    completed: bool = False