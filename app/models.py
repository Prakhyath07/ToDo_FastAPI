from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
    todos = relationship("ToDo", back_populates="owner")


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="todos")