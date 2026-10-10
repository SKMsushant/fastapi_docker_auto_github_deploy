from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import database_models,auth2,schemas,utils,database
from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/votes',
    tags=['votes']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    post=db.query(database_models.Post).filter(database_models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No post found with Post id {vote.post_id}")

    vote_query=db.query(database_models.Votes).filter(database_models.Votes.post_id==vote.post_id,database_models.Votes.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"you already voted on post {vote.post_id}")
        new_vote=database_models.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'vote added successfully'}
    elif vote.dir==0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'you never voted on post {vote.post_id}')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'vote removed successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="pass 0 to remove your vote and 1 to add your vote to the post")