from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, auth
from ..database import SessionLocal

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CartItem)
def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    return crud.add_to_cart(db, current_user.id, item)

@router.get("/", response_model=list[schemas.CartItem])
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    return crud.get_user_cart(db, current_user.id)

@router.delete("/{cart_id}")
def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    success = crud.remove_cart_item(db, cart_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item removed"}
