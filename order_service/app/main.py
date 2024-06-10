from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, database, security

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

@app.get("/validate-token/")
def validate_token(token: str = Depends(security.oauth2_scheme)):
    token_data = security.decode_access_token(token)
    return {"token_data": token_data}
