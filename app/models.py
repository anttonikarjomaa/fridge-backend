from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="household")
    inventory_items = relationship("InventoryItem", back_populates="household")
    shopping_items = relationship("ShoppingItem", back_populates="household")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    household_id = Column(Integer, ForeignKey("households.id"))

    household = relationship("Household", back_populates="users")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float, default=0)
    unit = Column(String, nullable=True)
    household_id = Column(Integer, ForeignKey("households.id"))

    household = relationship("Household", back_populates="inventory_items")


class ShoppingItem(Base):
    __tablename__ = "shopping_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float)
    unit = Column(String, nullable=True)
    household_id = Column(Integer, ForeignKey("households.id"))

    household = relationship("Household", back_populates="shopping_items")