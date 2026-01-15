from pydantic import BaseModel
from typing import List

class LogEntrySchema(BaseModel):
    hash: str
    message: str


class LogResponseSchema(BaseModel):
    logs: List[LogEntrySchema]
