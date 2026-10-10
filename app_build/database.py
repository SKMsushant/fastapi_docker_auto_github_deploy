from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from .config import settings

password = urllib.parse.quote_plus(settings.db_password)

SQLALCHEMY_DATABASE_URL=f"postgresql+psycopg2://{settings.db_username}:{password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(expire_on_commit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#import pyodbc
#from datetime import datetime
#import time

#database connection
#while True:
 #   try:
  #      server='localhost'
   #     database='fastapi'
    #    username='sa'
     #   password='SushantKumar@20081996'

      #  conn_str=pyodbc.connect(
       #     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
       #     f"SERVER={server};"
       #     f"DATABASE={database};"
       #     f"UID={username};"
       #     f"PWD={password};"
       #     f"TrustServerCertificate=yes;"
        #)

        #cursor=conn_str.cursor()
        #print('connection to database is successful')
        #break
    #except Exception as error:
     #   print('connection to database failed')
      #  print(f"Error : {error}")
       # time.sleep(10)
