from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..schemas import PostBase, TokenData, PostResponse, UserResponse, PostResponseVotes
from ..oauth2 import get_current_user
from ..models import User, Post, Vote
from typing import List


router = APIRouter(prefix="/posts",
                   tags=["Posts"])


# @router.get("/", response_model=List[PostResponse])
@router.get("/", response_model=List[PostResponseVotes])
def get_all_posts(search: str = "", limit: int = 10, skip: int = 0, db: Session=Depends(get_db)):
    
    posts = db.query(Post).all()
    
    posts = db.query(Post, func.count(Vote.user_id).label("votes"))\
        .join(Vote, Post.id == Vote.post_id, isouter=True).group_by(Post.id)\
        .filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # print([dict(r) for r in results])
    print(posts)
    
    return posts


# @router.get("/{id}", response_model=PostResponseVotes)
@router.get("/{id}")
def get_post(id: int, 
             db: Session=Depends(get_db), 
             current_user: TokenData = Depends(get_current_user)):
    
    # post = db.query(Post).get(id)
    post = db.query(Post, func.count(Vote.user_id).label("votes"))\
        .join(Vote, Post.id == Vote.post_id, isouter=True).group_by(Post.id)\
        .filter(Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id={id} does not exist.")
    elif post.Post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"This Post belongs to another User.")
    
    return post


@router.post("/", response_model=PostResponse)
def create_post(post_payload: PostBase, 
                db: Session=Depends(get_db),
                current_user: UserResponse = Depends(get_current_user)):
    
    new_post = Post(author_id=current_user.id, **post_payload.dict())

    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session=Depends(get_db),
                current_user: UserResponse = Depends(get_current_user)):
    
    post_to_delete = db.query(Post).get(id)
    
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id={id} does not exist.")
    elif post_to_delete.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Post with id={id} belongs to another user.")
        
    db.delete(post_to_delete)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int,
                post_payload: PostBase,
                db: Session=Depends(get_db),
                current_user: UserResponse = Depends(get_current_user)):
    
    update_query = db.query(Post).filter(Post.id == id)
    post_to_update = update_query.first()
    
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id={id} does not exist.")
    elif post_to_update.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Post with id={id} belongs to another user.")
        
    update_query.update(post_payload.dict())
    db.commit()
    
    db.refresh(post_to_update)
    
    return post_to_update