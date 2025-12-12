import time
import jwt
from config.settings import JWT_SECRET

def create_token(admin_id, org_id) -> str:
    now = int(time.time())
    payload = {"admin_id": str(admin_id), "org_id": str(org_id), "iat": now, "exp": now + 3600}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])  # type: ignore
    except Exception:
        return None

