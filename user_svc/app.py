import os
from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import auth, crud, database, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="QuickKart User Service")
bearer_scheme = HTTPBearer()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = auth.decode_token(creds.credentials)
        email: str = payload.get("sub")
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/register", response_model=schemas.UserOut, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    return user


@app.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_in.email)
    if not user or not auth.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token({"sub": user.email})
    return {"access_token": access_token}


@app.get("/verify", response_model=schemas.UserOut)
def verify_token(
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db),
):
    return get_current_user(creds, db)  # type: ignore[arg-type]


@app.get("/me", response_model=schemas.UserOut)
def me(current=Depends(get_current_user)):
    return current
