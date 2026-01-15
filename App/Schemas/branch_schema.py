from pydantic import BaseModel
from typing import List
from .commit_schema import CommitResponseSchema

class BranchCreateSchema(BaseModel):
    name: str


class BranchResponseSchema(BaseModel):
    name: str
    base: str
    commits: List[CommitResponseSchema]
