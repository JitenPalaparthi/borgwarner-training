from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, crud

router = APIRouter(prefix="/items", tags=["items"])

@router.post("", response_model=schemas.ItemOut, status_code=201)
def create(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_item(db, name=payload.name, description=payload.description, price=payload.price)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("", response_model=List[schemas.ItemOut])
def list_all(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return crud.list_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.ItemOut)
def read_one(item_id: int, db: Session = Depends(get_db)):
    obj = crud.get_item(db, item_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return obj

@router.patch("/{item_id}", response_model=schemas.ItemOut)
def patch(item_id: int, payload: schemas.ItemUpdate, db: Session = Depends(get_db)):
    try:
        obj = crud.update_item(db, item_id, name=payload.name, description=payload.description, price=payload.price)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return obj

@router.delete("/{item_id}", status_code=204)
def remove(item_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_item(db, item_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
