from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

# --------------------------
# GET all inventory items for a household
# --------------------------
@router.get("/{household_id}", response_model=List[schemas.InventoryItem])
def read_inventory_items(household_id: int, db: Session = Depends(get_db)):
    return crud.get_inventory_items(db, household_id)

# --------------------------
# GET a single inventory item by ID
# --------------------------
@router.get("/item/{item_id}", response_model=schemas.InventoryItem)
def read_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_inventory_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --------------------------
# POST create new inventory item
# --------------------------
@router.post("/", response_model=schemas.InventoryItem)
def create_inventory_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_item(db, item)

# --------------------------
# PATCH update existing inventory item
# --------------------------
@router.patch("/{item_id}", response_model=schemas.InventoryItem)
def update_inventory_item(item_id: int, item_update: schemas.InventoryItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_inventory_item(db, item_id, item_update)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --------------------------
# DELETE an inventory item
# --------------------------
@router.delete("/{item_id}", response_model=schemas.InventoryItem)
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_inventory_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item