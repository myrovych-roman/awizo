from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .user import User

Base = declarative_base()

class AvizationStatus(SAEnum):
    CREATED = "створена"
    ACTIVE = "активна"
    USED = "використана"
    EXPIRED = "прострочена"
    UNUSED = "не використана"

class AvizationType(SAEnum):
    DELIVERY = "доставка"
    GUEST = "гість"
    BUILDER = "будівельник"

class Avization(Base):
    __tablename__ = "avizations"

    id = Column(Integer, primary_key=True, index=True)
    car_number = Column(String, index=True)
    driver_name = Column(String)
    firm_name = Column(String)
    date_time = Column(DateTime)
    avization_type = Column(String)
    comment = Column(String)
    status = Column(String, default=AvizationStatus.CREATED)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
