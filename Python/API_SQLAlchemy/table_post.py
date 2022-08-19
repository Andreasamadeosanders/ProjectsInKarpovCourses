from sqlalchemy import Column, Integer, String, func, ForeignKey, DATETIME

from database import Base, SessionLocal

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)