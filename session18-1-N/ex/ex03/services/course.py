from ..models.course import Course

def get_all_course(db):
    return db.query(Course).all()

def create_course_service(data, db):
    data_course = data.model_dump()

    db_course = Course(**data_course)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course