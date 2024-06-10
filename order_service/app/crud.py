from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        user_id=order.user_id,
        from_station_id=order.from_station_id,
        to_station_id=order.to_station_id,
        status=1,  # status starts with 1 ("check")
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders_with_status(db: Session, status: int):
    return db.query(models.Order).filter(models.Order.status == status).all()

def update_order_status(db: Session, order: models.Order, new_status: int):
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
