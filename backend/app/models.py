from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class AdminModel(BaseModel):
    phone: str
    name: Optional[str]
    hashed_password: str
    role: str = "admin"  # 'owner' or 'admin'
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserModel(BaseModel):
    phone: str
    name: Optional[str]
    kyc_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AccountModel(BaseModel):
    user_phone: str
    currency: str = "AKZ"
    available_balance: float = 0.0
    reserved_balance: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionModel(BaseModel):
    txid: str
    from_phone: Optional[str]
    to_phone: Optional[str]
    amount: float
    currency: str = "AKZ"
    fee: float = 0.0
    status: str = "PENDING"  # PENDING / COMMITTED / REVERSED
    created_at: datetime = Field(default_factory=datetime.utcnow)