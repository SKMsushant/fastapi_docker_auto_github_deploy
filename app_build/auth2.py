from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from pydantic import EmailStr
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

from . import schemas

#secret_key
#algorithm
#expiration_time

SECRECT_KEY=settings.secret_key
ALGORITHM=settings.algorithm
EXPIRATION_TIME_MINUTES=settings.access_token_expire_minutes



oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data:dict):
    to_encode=data.copy()
    expire_at=datetime.now(timezone.utc)+timedelta(minutes=EXPIRATION_TIME_MINUTES)
    to_encode['exp']=expire_at

    encoded_jwt=jwt.encode(to_encode,SECRECT_KEY,ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credentials_exceptions):
    try:
        payload=jwt.decode(token,SECRECT_KEY,[ALGORITHM])

        email:EmailStr=payload.get('user_email')
        id:int=payload.get('user_id')
        if email is None:
            raise credentials_exceptions
        if id is None:
            raise credentials_exceptions
        
        token_data=schemas.TokenData(id=id,email=email)
        return token_data
    except JWTError:
        raise credentials_exceptions
    


def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exceptions=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials',headers={'WWW-Authenticate':'Bearer'})
    
    return verify_access_token(token,credentials_exceptions) 