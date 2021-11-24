from app import db
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, or_
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=1)
    avatar = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    products = relationship('Product', backref='user', lazy=True)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.username


class Category(BaseModel):
    name = Column(String(255), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    image = Column(String(100))
    price = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)

    def __str__(self):
        return self.name


class ReceiptDetail(BaseModel):
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), primary_key=True)
    unit_price = Column(Float, default=0)
    quantity = Column(Integer, default=0)


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    paid_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='receipt', lazy=True)


if __name__ == "__main__":
    pass