from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TransactionSource(Base):
    __tablename__ = "transaction_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    alt_name = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("transaction_source_categories.id"), nullable=True)

    # Відношення до категорії
    category = relationship("TransactionSourceCategory", back_populates="sources")
    # Відношення до фінансових рухів
    transactions = relationship("FinancialTransaction", back_populates="source")
