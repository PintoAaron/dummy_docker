from pydantic import BaseModel
from typing import Optional



class CustomerBase(BaseModel):
    name: str
    email: str