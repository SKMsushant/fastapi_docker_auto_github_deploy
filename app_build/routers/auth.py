from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from .. import database_models,database,schemas,utils,auth2

router=APIRouter(
    tags=['authentication']
)


@router.post('/login',response_model=schemas.Token)
def user_login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):

    user=db.query(database_models.CreateUser).filter(database_models.CreateUser.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    access_token=auth2.create_access_token(data={'user_id':user.id,'user_email':user.email})

    return {'access_token':access_token,'token_type':'bearer'}
    