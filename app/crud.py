from sqlalchemy.orm import Session
from . import models, schemas

# --------------------------
# Inventory CRUD
# --------------------------

def get_inventory_items(db: Session, household_id: int):
    return db.query(models.InventoryItem).filter(models.InventoryItem.household_id == household_id).all()

def get_inventory_item(db: Session, item_id: int):
    return db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()

def create_inventory_item(db: Session, item: schemas.InventoryItemCreate):
    db_item = models.InventoryItem(
        name=item.name,
        quantity=item.quantity,
        unit=item.unit,
        household_id=item.household_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_inventory_item(db: Session, item_id: int, item_update: schemas.InventoryItemUpdate):
    db_item = get_inventory_item(db, item_id)
    if not db_item:
        return None
    if item_update.quantity is not None:
        db_item.quantity = item_update.quantity
    if item_update.unit is not None:
        db_item.unit = item_update.unit
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_inventory_item(db: Session, item_id: int):
    db_item = get_inventory_item(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item


# --------------------------
# Shopping CRUD
# --------------------------

def get_shopping_items(db: Session, household_id: int):
    return db.query(models.ShoppingItem).filter(models.ShoppingItem.household_id == household_id).all()

def get_shopping_item(db: Session, item_id: int):
    return db.query(models.ShoppingItem).filter(models.ShoppingItem.id == item_id).first()

def create_shopping_item(db: Session, item: schemas.ShoppingItemCreate):
    db_item = models.ShoppingItem(
        name=item.name,
        quantity=item.quantity,
        unit=item.unit,
        household_id=item.household_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_shopping_item(db: Session, item_id: int, item_update: schemas.ShoppingItemUpdate):
    db_item = get_shopping_item(db, item_id)
    if not db_item:
        return None
    if item_update.quantity is not None:
        db_item.quantity = item_update.quantity
    if item_update.unit is not None:
        db_item.unit = item_update.unit
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_shopping_item(db: Session, item_id: int):
    db_item = get_shopping_item(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item


# --------------------------
# Shopping trip: move items to inventory
# --------------------------

def complete_shopping_trip(db: Session, household_id: int, item_ids: list[int]):
    """Move checked shopping items into inventory and remove them from shopping list."""
    for item_id in item_ids:
        shopping_item = get_shopping_item(db, item_id)
        if not shopping_item:
            continue

        # Check if item already exists in inventory
        inventory_item = db.query(models.InventoryItem).filter(
            models.InventoryItem.household_id == household_id,
            models.InventoryItem.name == shopping_item.name
        ).first()

        if inventory_item:
            inventory_item.quantity += shopping_item.quantity
        else:
            # Create new inventory item
            new_item = models.InventoryItem(
                name=shopping_item.name,
                quantity=shopping_item.quantity,
                unit=shopping_item.unit,
                household_id=household_id
            )
            db.add(new_item)

        # Remove from shopping list
        db.delete(shopping_item)

    db.commit()