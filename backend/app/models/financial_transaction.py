from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    details = Column(String(255), nullable=False)
    source_id = Column(Integer, ForeignKey("transaction_sources.id"), nullable=False)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    mcc = Column(Integer, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)

    # Відношення до джерела фінансового руху
    source = relationship("TransactionSource", back_populates="transactions")
    # Відношення до джерела даних
    data_source = relationship("DataSource", back_populates="transactions")
