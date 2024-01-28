from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

# Create a Base class using declarative_base(). Used to create the ORM models
Base = declarative_base()


from sqlalchemy import CheckConstraint

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    quantity = Column(Integer, nullable=False)
    is_delivered = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    __table_args__ = (UniqueConstraint("user_id", "product_id", "order_date", name="uk_key"),
                      CheckConstraint('quantity>=1 AND quantity<=100', name='quantity_range'),)



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True)
    user_name = Column(String, nullable=False,unique=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    orders = relationship("Order", back_populates="user")



class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="product")

    __table_args__ = (CheckConstraint('price>=100 AND price<=10000', name='price_range'),)