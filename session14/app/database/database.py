import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

raw_password = "a@1234"

encode_password = urllib.parse.quote_plus(raw_password)

DATABASE_URL = f"mysql+pymysql://root:{encode_password}@localhost:3306/session14" 

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()