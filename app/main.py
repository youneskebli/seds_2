
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users



@app.get("/orders/user/{user_id}", response_model=List[schemas.Order])
def read_user_orders(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    orders = crud.get_user_orders_delivered(db, user_id=user_id)
    return orders



@app.post("/users/new", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)



from fastapi import HTTPException

@app.post("/product/new", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if not 100 <= product.price <= 100000:
        raise HTTPException(status_code=400, detail="Price must be in the range [100, 10000]")
    try:
        return crud.create_product(db=db, product=product)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



@app.post("/orders/new/{user_id}/{product_id}", response_model=schemas.Order)
def create_order(user_id: int, product_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if not 1 <= order.quantity <= 100:
        raise HTTPException(status_code=400, detail="Quantity must be in the range [1, 100]")
    try:
        return crud.create_order(db=db, order=order, user_id=user_id, product_id=product_id)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    

@app.delete("/orders/delete/{product_name}/{user_id}/{order_date}")
def delete_order(product_name: str, user_id: int, order_date: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    product = crud.get_product_by_name(db, product_name=product_name)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    is_deleted = crud.delete_order(db=db, product_name=product_name, user_id=user_id, order_date=order_date)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Invalid order_date")
    return {"detail": "Order deleted"}