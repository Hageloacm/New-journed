import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/olaf")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-super-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
OWNER_PHONE = os.getenv("OWNER_PHONE", "+244900000000")  # teu número - o owner inicial