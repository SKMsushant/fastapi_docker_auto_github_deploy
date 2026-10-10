from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,Float,Identity,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP,DateTime
from sqlalchemy import text
from sqlalchemy.orm import relationship






class Post(Base):
    __tablename__='posts'
    id=Column(Integer,Identity(start=1,increment=1),primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="1",nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=text('now()'),nullable=False)
    owner=relationship('CreateUser')


class CreateUser(Base):
    __tablename__='users'

    id=Column(Integer,Identity(start=1,increment=1),primary_key=True,nullable=False)
    first_name=Column(String(100),nullable=False)
    middle_name=Column(String(100))
    last_name=Column(String(100),nullable=False)
    email=Column(String(255),unique=True,nullable=False)
    phone_number=Column(String(20),unique=True)
    password=Column(String(255),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=text('now()'),nullable=False)


class Votes(Base):
    __tablename__='votes'
    post_id=Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
    post_owner=relationship('Post')
    user_owner=relationship('CreateUser')