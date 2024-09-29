from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import User
from .. import models, schemas,utils, oauth2
from ..database import get_db



router = APIRouter(
    
    prefix="/api/v2/users",
    tags = ["Users"]

)


@router.get("/register", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def new_user_register(user_registration : schemas.UserCreate , db: Session = Depends(get_db)):
        user = db.query(models.User).filter(User.email == user_registration.email).first()
        if user:
                raise HTTPException(status = status.HTTP_403_FORBIDDEN , detail=f"User already registered with email {user_registration.email}")
        if not user:
            hashed_password = utils.hash(user_registration.password)
            new_user = User(email= user_registration.email, password=hashed_password,university= user_registration.university, course=user_registration.course, semester= user_registration.semester, skills= user_registration.skills)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        


@router.post("/login", response_model=schemas.Token)
def new_user_login(user_credentials:OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
       user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
       if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inavlid credentials")

       access_token = oauth2.create_access_token(data={"user_id": user.id})
       return {"access_token": access_token, "token_type": "bearer"}