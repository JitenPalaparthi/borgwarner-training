
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Item

def create_item(db: Session, *, name: str, description: str | None, price: float) -> Item:
    if db.execute(select(Item).where(Item.name == name)).scalar_one_or_none():
        raise ValueError("Item with this name already exists")
    obj = Item(name=name, description=description, price=price)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_item(db: Session, item_id: int) -> Item | None:
    return db.get(Item, item_id)

def list_items(db: Session, *, skip: int = 0, limit: int = 20) -> list[Item]:
    return db.execute(select(Item).offset(skip).limit(limit)).scalars().all()

def update_item(db: Session, item_id: int, *, name: str | None, description: str | None, price: float | None) -> Item | None:
    obj = db.get(Item, item_id)
    if not obj:
        return None
    if name is not None:
        # Check uniqueness excluding current record
        exists = db.execute(select(Item).where(Item.name == name, Item.id != item_id)).scalar_one_or_none()
        if exists:
            raise ValueError("Item with this name already exists")
        obj.name = name
    if description is not None:
        obj.description = description
    if price is not None:
        obj.price = price
    db.commit()
    db.refresh(obj)
    return obj

def delete_item(db: Session, item_id: int) -> bool:
    obj = db.get(Item, item_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
