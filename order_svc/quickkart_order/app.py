import asyncio

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from . import client, crud, database, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="QuickKart Order Service")
Instrumentator().instrument(app).expose(app)
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
async def make_order(order_in: schemas.OrderCreate,
                     email: str = Depends(get_current_user_email),
                     db: Session = Depends(get_db)):
    # validate product exists
    if not client.product_exists(order_in.item):
        raise HTTPException(status_code=404, detail="Item not in catalog")

    order = crud.create_order(db, email, order_in)
    # fire‑and‑forget email
    asyncio.create_task(client.email_confirmation(email, order_in.item))
    return order


@app.get("/orders", response_model=list[schemas.OrderOut])
def my_orders(
    email: str = Depends(get_current_user_email), db: Session = Depends(get_db)
):
    return crud.list_orders(db, email)
