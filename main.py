from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from database import engine, get_db
import models
from models import Customer
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "WELCOME HERE"}


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return {"data": customers}


@app.post("/customers", response_model=None)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    new_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"data": new_customer}
