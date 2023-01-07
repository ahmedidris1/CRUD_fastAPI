from pydantic import BaseModel
from pydantic import EmailStr
from pydantic.types import conint
from typing import Union
from datetime import datetime
from enum import IntEnum



class UserBase(BaseModel):
    email: EmailStr

class UserPayload(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    author: UserResponse
    
    class Config:
        orm_mode = True

class PostResponseVotes(BaseModel):
    Post: PostResponse
    votes: int
    
    class Config:
        orm_mode = True



class TokenData(BaseModel):
    id: Union[str, None]



# class VoteOptions(IntEnum):
#     like = 1
#     dislike = 0


class VoteBase(BaseModel):
    post_id: int
    vote_type: conint(le=1)

