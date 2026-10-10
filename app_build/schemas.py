from pydantic import BaseModel,EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from typing import Optional,Annotated,Union
from datetime import datetime
import phonenumbers





#POSTS

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    created_at:datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class UpdatePost(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    published:Optional[bool]=None
    created_at:datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class PostResponseOwnerInfo(BaseModel):
    id:int
    first_name:str
    middle_name:Optional[str]=None
    last_name:str
    email:EmailStr
    created_at:datetime

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    owner:PostResponseOwnerInfo
    class Config:
        from_attributes=True


###USERS
E164phonenumber=Annotated[Union[str,phonenumbers.PhoneNumber],PhoneNumberValidator(number_format='E164',default_region='IN')]

class CreateUser(BaseModel):
    first_name:str
    middle_name:Optional[str]=None
    last_name:Optional[str]=None
    email:EmailStr
    phone_number:Optional[E164phonenumber]=None
    password:str
    created_at:datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class ResponseUserInfo(BaseModel):
    first_name:str
    middle_name:Optional[str]=None
    last_name:Optional[str]
    email:EmailStr
    phone_number:Optional[E164phonenumber]=None
    created_at:datetime


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int
    email:Optional[EmailStr]=None

class Vote(BaseModel):
    post_id:int
    dir:int

class PostVoteResponse(PostResponse):
    votes:int