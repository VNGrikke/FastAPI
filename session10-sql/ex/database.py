import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database 

raw_password = "a@1234"
encoded_password = urllib.parse.quote_plus(raw_password)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost:3306/session10"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# --- THÊM ĐOẠN NÀY ĐỂ TỰ ĐỘNG TẠO DATABASE ---
if not database_exists(engine.url):
    create_database(engine.url)
    print("Đã tự động tạo database mới!")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()