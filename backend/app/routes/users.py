from fastapi import APIRouter, HTTPException, Depends, Header
from ..database import users_col, accounts_col
from ..schemas import TransactionRequest
from ..utils.security import decode_token
from ..utils.billing import compute_transaction_fee

router = APIRouter(prefix="/users", tags=["users"])

def get_requester_phone(authorization: str = Header(None)):
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    return payload.get("sub")

@router.post("/create")
async def create_user(data: dict):
    phone = data.get("phone")
    name = data.get("name")
    exists = await users_col.find_one({"phone": phone})
    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    await users_col.insert_one({"phone": phone, "name": name, "kyc_verified": False})
    # create default account
    await accounts_col.insert_one({"user_phone": phone, "currency": "AKZ", "available_balance": 0.0, "reserved_balance": 0.0})
    return {"phone": phone, "name": name}

@router.get("/balance/{phone}")
async def get_balance(phone: str):
    acc = await accounts_col.find_one({"user_phone": phone})
    if not acc:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"available": acc["available_balance"], "reserved": acc["reserved_balance"]}

@router.post("/transfer")
async def transfer(payload: TransactionRequest, requester=Depends(get_requester_phone)):
    # Simple server-side transfer (online)
    # verify accounts exist
    from_acc = await accounts_col.find_one({"user_phone": payload.from_phone})
    to_acc = await accounts_col.find_one({"user_phone": payload.to_phone})
    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Conta origem/destino não encontrada")
    if from_acc["available_balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    # compute fees
    fees = compute_transaction_fee(payload.amount, tx_type="transfer", currency=payload.currency, user_type="standard")
    # debit & credit
    await accounts_col.update_one({"user_phone": payload.from_phone}, {"$inc": {"available_balance": -payload.amount}})
    await accounts_col.update_one({"user_phone": payload.to_phone}, {"$inc": {"available_balance": fees["net"]}})
    # record transaction
    tx = {
        "txid": "tx_"+str(payload.from_phone)+str(payload.to_phone)+str(payload.amount),
        "from_phone": payload.from_phone,
        "to_phone": payload.to_phone,
        "amount": payload.amount,
        "currency": payload.currency,
        "fee": fees["fee"],
        "status": "COMMITTED"
    }
    await __import__("..database", fromlist=["transactions_col"]).transactions_col.insert_one(tx)
    # billing record
    await __import__("..database", fromlist=["billing_col"]).billing_col.insert_one({
        "txid": tx["txid"],
        "revenue": fees["fee"],
        "agent_cut": fees["agent_cut"],
        "timestamp": __import__("datetime").datetime.utcnow()
    })
    return {"detail":"Transferência executada", "txid": tx["txid"], "fee": fees}