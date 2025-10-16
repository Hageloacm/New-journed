from fastapi import FastAPI
from .routes import auth, admins, users, transactions
from .database import db, admins_col
from .utils.security import hash_password
from .config import OWNER_PHONE

app = FastAPI(title="OLAF Admin API", version="0.1")

app.include_router(auth.router)
app.include_router(admins.router)
app.include_router(users.router)
app.include_router(transactions.router)

@app.on_event("startup")
async def startup_event():
    # ensure owner exists (create on first run if missing)
    owner = await admins_col.find_one({"phone": OWNER_PHONE})
    if not owner:
        # temporary default password must be changed
        await admins_col.insert_one({
            "phone": OWNER_PHONE,
            "name": "Owner",
            "hashed_password": hash_password("change-owner-pass"),
            "role": "owner"
        })

@app.get("/")
async def root():
    return {"message":"OLAF Admin API running"}