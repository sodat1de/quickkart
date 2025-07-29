"""
Pure-unit CRUD test (in-memory SQLite).
No API, no docker-compose required.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from quickkart_product import crud, models, database, schemas

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)
models.Base.metadata.create_all(bind=engine)


def test_create_and_list_product():
    session = TestingSessionLocal()

    prod_in = schemas.ProductCreate(name="USB-C cable", description="1 m", price=9.99)
    created = crud.create_product(session, prod_in)

    assert created.id == 1
    assert created.name == "USB-C cable"

    products = crud.list_products(session)
    assert len(products) == 1
    assert products[0].name == prod_in.name
