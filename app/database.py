from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:lessgoReal@14Ucl@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
connect to db without sqlalchemy
'''
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
#
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='lessgoReal@14Ucl', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection successful")
#         break
#     except Exception as err:
#         print("databse conncetion failed")
#         print("error:", err)
#         time.sleep(5)
#
