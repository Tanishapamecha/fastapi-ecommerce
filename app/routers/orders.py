from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, auth
from ..database import SessionLocal

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Order)
def place_order(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    order = crud.place_order(db, current_user.id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return order

@router.get("/", response_model=list[schemas.Order])
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    return crud.get_user_orders(db, current_user.id)
