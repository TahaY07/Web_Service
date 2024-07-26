from fastapi import FastAPI, Depends, APIRouter, status
from pydantic import BaseModel

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

apps = FastAPI()

models.Base.metadata.create_all(engine)

router = APIRouter()

def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    id: int
    username: str


@router.get("/")
def home_page():
    return 'Welcome'



@router.get("/read", response_description="get_all")
def read_user(db: Session = Depends(get_db)):
    return db.query(models.User).all()


#?
@router.get("/read/{id}",response_description="by_id")
def read_user_by_id(sd: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter_by(id=sd)
    return result

#ok
@router.post("/create")
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.id = user.id
    user_model.username = user.username
    db.add(user_model)
    db.commit()
    return user


@router.put("/{id}")
def update_id(user: User, db: Session = Depends(get_db)):
    book_model = db.query(models.User).filter(models.User.id)
    db.add(book_model)
    db.commit()
    return user

#?
@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return 'Deleted'
    

apps.include_router(router)

