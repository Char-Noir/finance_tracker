from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class List(Base):
    __tablename__ = "lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False )
    author = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)