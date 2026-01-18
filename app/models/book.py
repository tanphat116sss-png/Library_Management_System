from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "BOOKS"

    book_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100))
    publisher = Column(String(100))
    publication_year = Column(Integer)
    category = Column(String(50))
    isbn = Column(String(20))
    quantity = Column(Integer)
    available_qty = Column(Integer)
    price = Column(DECIMAL(10, 2))

    borrow_records = relationship("BorrowRecord", back_populates="book")
