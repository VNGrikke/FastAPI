from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse
from sqlalchemy_utils import database_exists, create_database


raw_password = "a@1234"
encode_password = urllib.parse.quote(raw_password) # xu li mat khau vi co chua "@"

DATABASE_URL = f"mysql+pymysql://root:{encode_password}@localhost:3306/session12"

engine = create_engine(DATABASE_URL) # Ket noi voi database

if not database_exists(engine.url): # Kiem tra ton tai database (Khon co thi tao moi)
    create_database(engine.url)
    
SessionLocal = sessionmaker(
    autoflush= False,
    autocommit= False,
    bind= engine
)

Base = declarative_base()
