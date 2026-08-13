import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

raw_password = "a@1234" 
encode_password = urllib.parse.quote_plus(raw_password)

DATABASE_URL = f"mysql+pymysql://root:{encode_password}@127.0.0.1:3306/product_db"

engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()