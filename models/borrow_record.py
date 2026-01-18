from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BorrowRecord(Base):
    __tablename__ = "BORROW_RECORDS"

    record_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("USERS.user_id"))
    book_id = Column(Integer, ForeignKey("BOOKS.book_id"))

    borrow_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date)
    book_status = Column(String(50))

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
    fine = relationship("Fine", back_populates="borrow_record", uselist=False)