from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel,EmailStr
from typing import Optional,List
import random
import pyodbc
from datetime import datetime
import time
from sqlalchemy import func

from .. import database_models,schemas,utils,auth2
from ..database import engine,get_db
from sqlalchemy.orm import Session


router=APIRouter(
    prefix="/posts",
    tags=['posts']
)




#to send all posts to the user
@router.get("/",response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user),search:Optional[str]=""):
    #cursor.execute(""" select * from posts""")
    #columns=[col[0] for col in cursor.description]
    #posts=[dict(zip(columns,row)) for row in cursor.fetchall()]
    posts=db.query(database_models.Post).filter(database_models.Post.title.contains(search)).all()

    vote_query=db.query(
        database_models.Post.id,
        func.count(
            database_models.Votes.user_id
            ).label("Votes")).join(
                database_models.Votes,isouter=True
                ).group_by(
                    database_models.Post.id).all()
    vote_map={post_id:vote_count for post_id,vote_count in vote_query}
    for post in posts:
        post.votes=vote_map.get(post.id)
    

    return posts

#to send user's own posts
@router.get("/my_posts",response_model=List[schemas.PostVoteResponse])
def get_my_posts(db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    posts=db.query(database_models.Post).filter(database_models.Post.user_id==current_user.id).all()

    vote_query=db.query(
            database_models.Post.id,
            func.count(
                database_models.Votes.user_id
                ).label("Votes")).join(
                    database_models.Votes,isouter=True
                    ).group_by(
                        database_models.Post.id
                        ).filter(
                            database_models.Post.user_id==current_user.id
                            ).all()
    
    vote_map={post_id:vote_count for post_id,vote_count in vote_query}
    for post in posts:
        post.votes=vote_map.get(post.id)
    return posts


#to send one post to the user
@router.get('/{id}',response_model=schemas.PostVoteResponse)
def get_post(id:int,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    #cursor.execute("""select * from posts where id=?""",(id))
    #columns=[col[0] for col in cursor.description]
    #one_post=dict(zip(columns,cursor.fetchone()))
    one_post=db.query(database_models.Post).filter(database_models.Post.id==id).first()
    
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} not found")
    else:
        vote_query=db.query(
                        database_models.Post.id,
                        func.count(
                            database_models.Votes.user_id
                            ).label("Votes")).join(
                                database_models.Votes,isouter=True
                                ).group_by(
                                    database_models.Post.id
                                    ).filter(database_models.Post.id==id).first()
        one_post.votes=vote_query[1]
        return one_post


#to retrieve post from user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(userdata:schemas.Post,db: Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    #cursor.execute("""insert into posts (title,content) output inserted.* values (?,?) """,(userdata.title,userdata.content))
    #columns=[col[0] for col in cursor.description]
    #new_post=dict(zip(columns,cursor.fetchone()))
    #conn_str.commit()
    post_data=userdata.model_dump(exclude_unset=True)
    new_post=database_models.Post(**post_data)
    new_post.user_id=current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




#to delete one post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    #cursor.execute("""delete from posts output deleted.* where id=?""",(id))
    #deleted_post=cursor.fetchone()
    #conn_str.commit()

    post_query=db.query(database_models.Post).filter(database_models.Post.id==id)

    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    if post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()


#to update one post
@router.put('/{id}',response_model=schemas.PostVoteResponse)
def update_post(id:int,post:schemas.UpdatePost,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(auth2.get_current_user)):
    update_data=post.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided to update")
    #set_clause=', '.join([f"{key}=?" for key in update_data.keys()])
    #values=list(update_data.values())+[id]
    #query=f"update posts set {set_clause} output inserted.* where id=?"
    #cursor.execute(query,tuple(values))
    #row=cursor.fetchone()
    #if row==None:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
   # #columns=[col[0] for col in cursor.description]
    #updated_post=dict(zip(columns,row))
    #conn_str.commit()

    post_query=db.query(database_models.Post).filter(database_models.Post.id==id)
    post_item=post_query.first()
    if post_item==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} not found")

    if post_item.user_id !=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")

    post_query.update(update_data,synchronize_session=False)
    db.commit()
    db.refresh(post_item)
    #updated_post=db.query(database_models.Post).filter(database_models.Post.id==id).first()
    vote_query=db.query(
                        database_models.Post.id,
                        func.count(
                            database_models.Votes.user_id
                            ).label("Votes")).join(
                                database_models.Votes,isouter=True
                                ).group_by(
                                    database_models.Post.id
                                    ).filter(database_models.Post.id==id).first()
    post_item.votes=vote_query[1]

    return post_item