from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import crud, models, schemas, security, database
from pydantic import ValidationError

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        new_user = crud.create_user(db=db, user=user)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = security.create_access_token(data={"sub": user.email})
    crud.create_user_session(db, user_id=user.id, token=access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = security.decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    session = crud.get_user_by_token(db, token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    user = crud.get_user_by_email(db, email=token_data.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
