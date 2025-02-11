from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class TransactionSourceCategory(Base):
    __tablename__ = "transaction_source_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    color = Column(String(7), nullable=False)

    # Відношення до джерел фінансового руху
    sources = relationship("TransactionSource", back_populates="category")

