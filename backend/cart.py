from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from models import Cart, Product, User
from users import get_current_user, get_db  # Assuming these are defined elsewhere
from pydantic import BaseModel
from typing import List



router = APIRouter()

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    employee_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    cost: float

    class Config:
        orm_mode = True


class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int

    class Config:
        orm_mode = True



@router.post("/cart/", response_model=CartItemResponse)
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(
        Cart.employee_id == cart_item.employee_id, 
        Cart.product_id == cart_item.product_id
    ).first()

    if db_cart_item:
        db_cart_item.quantity += cart_item.quantity
    else:
        db_cart_item = Cart(
            employee_id=cart_item.employee_id, 
            product_id=cart_item.product_id, 
            quantity=cart_item.quantity
        )
        db.add(db_cart_item)

    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item



@router.get("/cart/", response_model=List[CartItemResponse])
def get_cart(
    employee_id: int = Query(...),
    db: Session = Depends(get_db),
):
    cart_items = (
        db.query(Cart)
        .filter(Cart.employee_id == employee_id)  # Проверка по employee_id
        .join(Product, Product.id == Cart.product_id)
        .all()
    )

    if not cart_items:
        raise HTTPException(status_code=404, detail="No items found for this employee")
    
    return cart_items


@router.put("/cart/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: int, cart_item: CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(
        Cart.id == cart_item_id, 
        Cart.employee_id == cart_item.employee_id
    ).first()

    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db_cart_item.quantity = cart_item.quantity
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item


