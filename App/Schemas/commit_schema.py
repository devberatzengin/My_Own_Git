from pydantic import BaseModel

class CommitCreateSchema(BaseModel):
    message: str

class CommitResponseSchema(BaseModel):
    hash: str
    message: str
