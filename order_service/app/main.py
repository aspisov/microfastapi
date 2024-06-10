from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import crud, models, schemas, database, security
import asyncio
import random

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, token: str = Depends(security.oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = security.decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return crud.create_order(db=db, order=order)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, token: str = Depends(security.oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = security.decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    order = crud.get_order(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

async def process_orders():
    while True:
        await asyncio.sleep(10)  # wait for 10 seconds
        db = next(database.get_db())
        orders = crud.get_orders_with_status(db, status=1)  # status 1 is "check"
        for order in orders:
            new_status = random.choice([2, 3])  # randomly choose between "success" (2) and "rejection" (3)
            crud.update_order_status(db, order, new_status)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_orders())
