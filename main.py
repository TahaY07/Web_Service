from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from pydantic import BaseModel

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

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



@router.get("/read/{id}",response_description="by_id")
def read_user_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id==id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/create")
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.id = user.id
    user_model.username = user.username
    db.add(user_model)
    db.commit()
    return user


@router.put("/{id}/{newid}")
def update_id(id:int, newid:int, db: Session = Depends(get_db)):
    
    user_model = db.query(models.User).filter(models.User.id == id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_model.id = newid
    db.commit()
    return user_model


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db.delete(user)
        db.commit()
        return {"detail":"Deleted"}
    

app.include_router(router)
