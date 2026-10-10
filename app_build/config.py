from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path

env_file_path=Path(__file__).resolve().parent.parent/".env"

class Settings(BaseSettings):
    db_hostname:str
    db_password:str
    db_username:str
    db_port:str
    db_name:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    model_config=SettingsConfigDict(
        env_file=str(env_file_path),
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings=Settings()