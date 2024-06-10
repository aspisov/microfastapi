from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    user_id: int
    from_station_id: int
    to_station_id: int
    status: int

class Order(BaseModel):
    id: int
    user_id: int
    from_station_id: int
    to_station_id: int
    status: int
    created_at: datetime

    class Config:
        orm_mode = True
