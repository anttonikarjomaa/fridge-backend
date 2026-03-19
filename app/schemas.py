from pydantic import BaseModel
from typing import Optional

# --------------------------
# Inventory schemas
# --------------------------

class InventoryItemBase(BaseModel):
    name: str
    quantity: float
    unit: Optional[str] = None

class InventoryItemCreate(InventoryItemBase):
    household_id: int

class InventoryItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit: Optional[str] = None

class InventoryItem(InventoryItemBase):
    id: int
    household_id: int

    class Config:
        orm_mode = True


# --------------------------
# Shopping schemas
# --------------------------

class ShoppingItemBase(BaseModel):
    name: str
    quantity: float
    unit: Optional[str] = None

class ShoppingItemCreate(ShoppingItemBase):
    household_id: int

class ShoppingItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit: Optional[str] = None

class ShoppingItem(ShoppingItemBase):
    id: int
    household_id: int

    class Config:
        orm_mode = True