from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text("now()"), 
                        nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    author_id = Column(Integer, 
                       ForeignKey("users.id", 
                                  ondelete="CASCADE",
                                  onupdate="CASCADE"), 
                       nullable=False)
    author = relationship("User", back_populates="posts")
    # votes = relationship("Vote", back_populates="post")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text("now()"), 
                        nullable=False)
    posts = relationship("Post", back_populates="author")




class Vote(Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), 
                     primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), 
                     primary_key=True, nullable=False)
    # post = relationship("Post", back_populates="votes")