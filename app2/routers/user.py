from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserPayload, UserResponse
from ..models import User
from ..utils import hash_password
from ..oauth2 import get_current_user


router = APIRouter(prefix="/users",
                   tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserPayload, db: Session=Depends(get_db)):
    
    user = db.query(User).filter(User.email == payload.email).first()
    
    if user is None:
        new_user = User(**payload.dict())
        new_user.password = hash_password(payload.password)
        db.add(new_user)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="There is already a user with such an email.")
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, 
             db: Session=Depends(get_db), 
             current_user: UserResponse = Depends(get_current_user)):
    
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={id} does not exist.")
    elif current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are trying to retrieve Info that does not belong to you.")
        
    return user