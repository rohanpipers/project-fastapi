from fastapi import status, HTTPException, Depends, APIRouter

from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hased_password = utils.hash(user.password)
    user.password = hased_password

    newuser = models.User(**user.dict())
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = f"post with id: {id} does not exist")

    return user
