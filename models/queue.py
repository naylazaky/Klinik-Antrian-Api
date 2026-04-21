from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Queue(Base):
    __tablename__ = "queues"

    id           = Column(Integer, primary_key=True, index=True)
    queue_number = Column(Integer, nullable=False)
    status       = Column(String, default="waiting")
    complaint    = Column(String, nullable=True)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="queues")