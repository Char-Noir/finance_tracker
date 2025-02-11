from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel

# Таблиця джерело даних руху
class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    transactions = relationship("FinancialTransaction", back_populates="data_source")

# Таблиця категорія джерела фінансового руху
class TransactionSourceCategory(Base):
    __tablename__ = "transaction_source_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    color = Column(String(7), nullable=True)  # Зберігати колір у форматі HEX

    sources = relationship("TransactionSource", back_populates="category")

# Таблиця джерело фінансового руху
class TransactionSource(Base):
    __tablename__ = "transaction_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    alt_name = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("transaction_source_categories.id"), nullable=False)

    category = relationship("TransactionSourceCategory", back_populates="sources")
    transactions = relationship("FinancialTransaction", back_populates="transaction_source")

# Таблиця фінансовий рух
class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    details = Column(String(255), nullable=False)
    transaction_source_id = Column(Integer, ForeignKey("transaction_sources.id"), nullable=True)
    mcc = Column(String(4), nullable=True)
    amount_card_currency = Column(Float, nullable=False)
    amount_transaction_currency = Column(Float, nullable=True)
    currency = Column(String(10), nullable=True)
    exchange_rate = Column(Float, nullable=True)
    commission_uah = Column(Float, nullable=True)
    cashback_uah = Column(Float, nullable=True)
    balance_after_transaction = Column(Float, nullable=True)

    data_source = relationship("DataSource", back_populates="transactions")
    transaction_source = relationship("TransactionSource", back_populates="transactions")



# Pydantic модель для вхідних даних
class DataSourceCreate(BaseModel):
    name: str
