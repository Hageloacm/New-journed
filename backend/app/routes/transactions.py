from fastapi import APIRouter, HTTPException
from ..database import transactions_col, billing_col
from ..schemas import TransactionRequest
from ..utils.billing import compute_transaction_fee
import uuid, datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/create")
async def create_tx(payload: TransactionRequest):
    txid = str(uuid.uuid4())
    fees = compute_transaction_fee(payload.amount, tx_type="transfer", currency=payload.currency)
    tx = {
        "txid": txid,
        "from_phone": payload.from_phone,
        "to_phone": payload.to_phone,
        "amount": payload.amount,
        "currency": payload.currency,
        "fee": fees["fee"],
        "status": "PENDING",
        "created_at": datetime.datetime.utcnow()
    }
    await transactions_col.insert_one(tx)
    # pretend processing: immediately commit for MVP
    await transactions_col.update_one({"txid": txid}, {"$set": {"status": "COMMITTED"}})
    await billing_col.insert_one({
        "txid": txid,
        "revenue": fees["fee"],
        "agent_cut": fees["agent_cut"],
        "timestamp": datetime.datetime.utcnow()
    })
    return {"txid": txid, "fee": fees}