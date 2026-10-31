from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base  # Absolute import

class GuestbookEntry(Base):
    __tablename__ = "guestbook_entries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)