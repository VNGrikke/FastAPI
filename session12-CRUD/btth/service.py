import models
from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_all_documents_service(db: Session):
    documents = db.query(models.DocumentModel).all()
    return {
        "message": "Lấy danh sách tài liệu thành công",
        "data": documents
    }

def create_document_service(db: Session, doc_data):
    """Xử lý logic thêm tài liệu mới"""
    new_document = models.DocumentModel(
        title=doc_data.title,
        subject=doc_data.subject,
        document_type=doc_data.document_type,
        file_url=doc_data.file_url
    )
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document) 
    
    return {
        "message": "Thêm tài liệu thành công",
        "data": new_document
    }

def delete_document_service(db: Session, document_id: int):
    """Xử lý logic kiểm tra và xóa tài liệu"""
    document = db.query(models.DocumentModel).filter(models.DocumentModel.id == document_id).first()
    
    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Tài liệu không tồn tại trong hệ thống"
        )
    
    deleted_data = {
        "id": document.id,
        "title": document.title
    }
    
    db.delete(document)
    db.commit()
    
    return {
        "message": "Xóa tài liệu thành công",
        "data": deleted_data
    }