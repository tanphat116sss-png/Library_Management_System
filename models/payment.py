from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = "PAYMENTS"

    payment_id = Column(Integer, primary_key=True)
    fine_id = Column(Integer, ForeignKey("FINES.fine_id"))
    amount = Column(DECIMAL(10, 2))
    payment_method = Column(String(50))
    payment_date = Column(
        TIMESTAMP, server_default=func.current_timestamp()
    )

    fine = relationship("Fine", back_populates="payments")
