from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QueueCreate(BaseModel):
    complaint: Optional[str] = None

class QueueUpdate(BaseModel):
    status: str

class QueueOut(BaseModel):
    id: int
    queue_number: int
    status: str
    complaint: Optional[str]
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True