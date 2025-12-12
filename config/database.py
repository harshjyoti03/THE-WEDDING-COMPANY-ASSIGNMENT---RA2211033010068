from pymongo import MongoClient, ASCENDING
from .settings import MONGO_URI, MASTER_DB_NAME, TENANT_DB_NAME

client = MongoClient(MONGO_URI)
master_db = client[MASTER_DB_NAME]
tenant_db = client[TENANT_DB_NAME]
orgs = master_db["organizations"]
admins = master_db["admins"]

orgs.create_index([("name", ASCENDING)], unique=True)
orgs.create_index([("collection_name", ASCENDING)], unique=True)
admins.create_index([("email", ASCENDING)], unique=True)

