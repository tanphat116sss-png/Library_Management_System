from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "USERS"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    user_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    email = Column(String(100))
    user_role = Column(String(20))
    is_active = Column(String(10))

    borrow_records = relationship("BorrowRecord", back_populates="user")
