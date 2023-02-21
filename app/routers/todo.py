from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/todos",
    tags=['ToDos']
)



@router.get("/", response_model=List[schemas.ToDoOut])
def get_all(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    todos = db.query(models.ToDo).filter(models.ToDo.owner_id == current_user.id).all()
    return todos
   
    


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ToDoOut)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_todo = models.ToDo(owner_id=current_user.id, **todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/{id}", response_model=schemas.ToDoOut)
def get_todo(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    

    todo_query = db.query(models.ToDo).filter(models.ToDo.id == id)

    todo = todo_query.first()
    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"todo with id: {id} does not exist")

    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return todo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    todo_query = db.query(models.ToDo).filter(models.ToDo.id == id)

    todo = todo_query.first()

    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"todo with id: {id} does not exist")

    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    todo_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.ToDoOut)
def update_todo(id: int, updated_post: schemas.ToDoCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    todo_query = db.query(models.ToDo).filter(models.ToDo.id == id)

    todo = todo_query.first()

    if todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"todo with id: {id} does not exist")

    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    todo_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return todo_query.first()