from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    data_encoded = data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    data_encoded["exp"] = expiration_time
    
    access_token = jwt.encode(data_encoded, settings.secret_key, settings.algorithm)
    
    return access_token



def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
        # user_id = payload.get("user_id")
        
        # if not user_id:
        #     raise credentials_exception
        
        # token_data = TokenData(id = user_id)
        token_data = TokenData(**payload)
        
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Invalid credentials.")
    
    token_data = verify_access_token(token=token, 
                                  credentials_exception=credentials_exception)
    
    user = db.query(User).filter(User.id == token_data.id).first()
    
    return user