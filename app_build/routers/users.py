from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel,EmailStr
from typing import Optional,List
import random

from datetime import datetime
import time


from .. import database_models,schemas,utils,auth2
from ..database import engine,get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/users",
    tags=['users']
)



@router.post('/createusers',status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseUserInfo)
def create_user(user:schemas.CreateUser,db:Session=Depends(get_db)):
    userdata=user.model_dump(exclude_unset=True)
    user_email=userdata['email']
    existing_emails=[]
    for email in db.query(database_models.CreateUser.email).all():
        existing_emails.append(email[0])
    if user_email in existing_emails:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"email {user_email} is already registered")
    hashed_password=utils.hash_password(userdata['password'])
    userdata['password']=hashed_password

    new_user=database_models.CreateUser(**userdata)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{email}",response_model=schemas.ResponseUserInfo)
def get_user(email:EmailStr,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    user=db.query(database_models.CreateUser).filter(database_models.CreateUser.email==email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with email : {email} not found')

    return user