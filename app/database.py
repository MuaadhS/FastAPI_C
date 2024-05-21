from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

#print(settings.dict())

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:0102030405@localhost:5433/fastapi'

#print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Connection to DB
# This method is not used it's here for reference
# The database is connected using sqlalchemy above
'''
while True:
    try:
        conn = psycopg2.connect(host='localhost', port=5433, database='fastapi',
                               user='postgres', password='0102030405',
                               cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection is successful")
        break

    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(3)
'''