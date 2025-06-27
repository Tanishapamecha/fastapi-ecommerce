from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_ecommerce import schemas, crud
from fastapi_ecommerce.database import SessionLocal
from fastapi_ecommerce.auth import get_current_user
from fastapi_ecommerce.models import User

router = APIRouter(prefix="/products", tags=["Products"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 only logged-in users
):
    return crud.create_product(db=db, product=product)


@router.get("/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)






# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuaWRoaSIsImV4cCI6MTc1MTAwNDcyNH0.6xUfBJDQRmr7igYN7PtulNHHuLZoI_pChDudu55WHEo",
#   "token_type": "bearer"
# } 