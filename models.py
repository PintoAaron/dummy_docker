from database import Base
import sqlalchemy


class Customer(Base):
    __tablename__ = "customers"
    customer_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False)
