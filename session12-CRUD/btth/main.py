from fastapi import FastAPI, Depends
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session
from service import get_all_documents_service, create_document_service, delete_document_service
from pydantic import BaseModel


models.Base.metadata.create_all(engine)

class DocumentCreate(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str

app = FastAPI(title="Learning Document Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    return get_all_documents_service(db)

@app.post("/documents")
def create_document(doc_data: DocumentCreate, db: Session = Depends(get_db)):
    return create_document_service(db, doc_data)

@app.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    return delete_document_service(db, document_id)