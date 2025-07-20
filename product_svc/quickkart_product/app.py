from fastapi import Depends, FastAPI, HTTPException

from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from . import crud, database, models, schemas

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="QuickKart Product Service")
Instrumentator().instrument(app).expose(app)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/products", response_model=schemas.ProductOut, status_code=201)
def add_product(prod_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    if db.query(models.Product).filter(models.Product.name == prod_in.name).first():
        raise HTTPException(status_code=400, detail="Name already exists")
    return crud.create_product(db, prod_in)

@app.get("/products", response_model=list[schemas.ProductOut])
def all_products(db: Session = Depends(get_db)):
    return crud.list_products(db)