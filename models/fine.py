from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Fine(Base):
    __tablename__ = "FINES"

    fine_id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey("BORROW_RECORDS.record_id"))
    fine_date = Column(
        TIMESTAMP, server_default=func.current_timestamp()
    )
    paid_status = Column(String(20))
    fine_amount = Column(DECIMAL(10, 2))

    borrow_record = relationship("BorrowRecord", back_populates="fine")
    payments = relationship("Payment", back_populates="fine")
