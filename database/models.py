from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)

    expenses = relationship("Expense", back_populates="user")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="category")


class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    symbol = Column(String)

    expenses = relationship("Expense", back_populates="currency")


class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    currency = relationship("Currency", back_populates="expenses")
