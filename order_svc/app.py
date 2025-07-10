import asyncio
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import client, crud, database, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="QuickKart Order Service")
bearer_scheme = HTTPBearer()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


async def get_current_user_email(
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    try:
        data = await client.validate_jwt(creds.credentials)
        return data["email"]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@app.post("/orders", response_model=schemas.OrderOut, status_code=201)
async def make_order(
    order_in: schemas.OrderCreate,
    email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db),
):
    return crud.create_order(db, email, order_in)


@app.get("/orders", response_model=list[schemas.OrderOut])
def my_orders(
    email: str = Depends(get_current_user_email), db: Session = Depends(get_db)
):
    return crud.list_orders(db, email)
