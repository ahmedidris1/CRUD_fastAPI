from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserResponse, VoteBase
from ..oauth2 import get_current_user
from ..models import Vote


router = APIRouter(tags=["Votes"])


@router.post("/vote")
def vote(vote_payload: VoteBase,
         db: Session = Depends(get_db), 
         current_user: UserResponse = Depends(get_current_user)):
    
    vote_query = db.query(Vote).filter(Vote.user_id == current_user.id, 
                                       Vote.post_id == vote_payload.post_id)
    existing_vote = vote_query.first()
    
    if (vote_payload.vote_type == 1):
        
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="You can not vote twice for the same post.")
            
        new_vote = Vote(post_id=vote_payload.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {
            "message": "successfully added a vote."
        }
        
    else:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"You can't remove a vote that you haven't already placed.")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
    
        return {
            "message": "successfully deleted vote."
        }
    