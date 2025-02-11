from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    # Відношення до фінансових рухів
    transactions = relationship("FinancialTransaction", back_populates="data_source")
