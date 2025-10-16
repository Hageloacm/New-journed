from pydantic import BaseModel
from typing import Optional, List

class LoginRequest(BaseModel):
    phone: str
    password: str

class AdminCreate(BaseModel):
    phone: str
    name: Optional[str]
    password: str
    role: Optional[str] = "admin"

class AdminOut(BaseModel):
    phone: str
    name: Optional[str]
    role: str

class TransactionRequest(BaseModel):
    from_phone: str
    to_phone: str
    amount: float
    currency: Optional[str] = "AKZ"