from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..utils import hash_password, verify_password
from ..oauth2 import create_access_token


router = APIRouter(tags=["Auth"])


@router.post('/login')
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db) ):
    
    user = db.query(User).filter(User.email == payload.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials.")
    
    is_authenticated = verify_password(payload.password, user.password)
    
    if not is_authenticated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials.")
        
    access_token = create_access_token(data={"id": user.id})
        
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }