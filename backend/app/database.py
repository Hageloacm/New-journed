from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()

# Collections
admins_col = db["admins"]
users_col = db["users"]
accounts_col = db["accounts"]
transactions_col = db["transactions"]
agents_col = db["agents"]
billing_col = db["billing"]