from pydantic import BaseModel

class InitRepositorySchema(BaseModel):
    path: str
