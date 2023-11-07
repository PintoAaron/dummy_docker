from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "WELCOME HERE"}


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return {"data": customers}
