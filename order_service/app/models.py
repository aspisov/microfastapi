from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    from_station_id = Column(Integer)
    to_station_id = Column(Integer)
    status = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
