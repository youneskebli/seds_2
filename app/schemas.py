from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    orders: List['Order'] = []

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    product_name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    orders: List['Order'] = []

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    delivered: Optional[bool] = False

    class Config:
        orm_mode = True