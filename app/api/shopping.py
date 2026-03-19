from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/shopping",
    tags=["shopping"]
)

# --------------------------
# GET all shopping items for a household
# --------------------------
@router.get("/{household_id}", response_model=List[schemas.ShoppingItem])
def read_shopping_items(household_id: int, db: Session = Depends(get_db)):
    return crud.get_shopping_items(db, household_id)

# --------------------------
# GET a single shopping item by ID
# --------------------------
@router.get("/item/{item_id}", response_model=schemas.ShoppingItem)
def read_shopping_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_shopping_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --------------------------
# POST create new shopping item
# --------------------------
@router.post("/", response_model=schemas.ShoppingItem)
def create_shopping_item(item: schemas.ShoppingItemCreate, db: Session = Depends(get_db)):
    return crud.create_shopping_item(db, item)

# --------------------------
# PATCH update existing shopping item
# --------------------------
@router.patch("/{item_id}", response_model=schemas.ShoppingItem)
def update_shopping_item(item_id: int, item_update: schemas.ShoppingItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_shopping_item(db, item_id, item_update)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --------------------------
# DELETE a shopping item
# --------------------------
@router.delete("/{item_id}", response_model=schemas.ShoppingItem)
def delete_shopping_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_shopping_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --------------------------
# Complete shopping trip: move items into inventory
# --------------------------
@router.post("/complete")
def complete_shopping_trip(household_id: int, item_ids: List[int], db: Session = Depends(get_db)):
    crud.complete_shopping_trip(db, household_id, item_ids)
    return {"message": "Shopping trip completed and items added to inventory."}