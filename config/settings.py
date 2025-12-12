import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MASTER_DB_NAME = os.environ.get("MASTER_DB_NAME", "master_db")
TENANT_DB_NAME = os.environ.get("TENANT_DB_NAME", "tenant_db")
JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret")

