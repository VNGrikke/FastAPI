from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse
from sqlalchemy_utils import database_exists, create_database

raw_password = "a@1234"
encode_password = urllib.parse.quote(raw_password)

DATABASE_URL = f"mysql+pymysql://root:{encode_password}@localhost:3306/session12"

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
    
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()