import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.orm import sessionmaker, declarative_base

raw_password = "a@1234"
encode_password = urllib.parse.quote_plus(raw_password)

DATABASE_URL = f"mysql+pymysql://root:{encode_password}@localhost:3306/ss18"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()