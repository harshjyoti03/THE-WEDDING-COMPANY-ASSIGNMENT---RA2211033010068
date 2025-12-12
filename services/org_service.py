from pymongo.errors import CollectionInvalid
from config.database import tenant_db, orgs, admins
from models.organization_model import collection_name_for, serialize_org
from utils.password_helper import hash_password, check_password
import time

def create_org(name: str, email: str, password: str):
    if orgs.find_one({"name": name}):
        return 409, {"error": "organization already exists"}
    if admins.find_one({"email": email}):
        return 409, {"error": "admin email already in use"}
    col_name = collection_name_for(name)
    try:
        tenant_db.create_collection(col_name)
    except CollectionInvalid:
        return 409, {"error": "organization collection already exists"}
    org_doc = {
        "name": name,
        "collection_name": col_name,
        "connection": {"db": tenant_db.name},
        "created_at": int(time.time()),
    }
    org_res = orgs.insert_one(org_doc)
    org_id = org_res.inserted_id
    pwd_hash = hash_password(password)
    admin_doc = {
        "email": email,
        "password_hash": pwd_hash,
        "org_id": org_id,
        "created_at": int(time.time()),
    }
    admin_res = admins.insert_one(admin_doc)
    admin_id = admin_res.inserted_id
    orgs.update_one({"_id": org_id}, {"$set": {"admin_id": admin_id}})
    return 201, {"message": "organization created", "organization": serialize_org({"_id": org_id, **org_doc, "admin_id": admin_id})}

def get_org_by_name(name: str):
    doc = orgs.find_one({"name": name})
    if not doc:
        return 404, {"error": "organization not found"}
    return 200, {"organization": serialize_org(doc)}

def update_org(new_name: str, email: str, password: str):
    admin_doc = admins.find_one({"email": email})
    if not admin_doc:
        return 401, {"error": "invalid credentials"}
    if not check_password(password, admin_doc.get("password_hash")):
        return 401, {"error": "invalid credentials"}
    org_id = admin_doc.get("org_id")
    org_doc = orgs.find_one({"_id": org_id})
    if not org_doc:
        return 404, {"error": "organization not found"}
    if org_doc.get("name") == new_name:
        return 200, {"message": "no changes", "organization": serialize_org(org_doc)}
    if orgs.find_one({"name": new_name}):
        return 409, {"error": "organization name already exists"}
    old_col = org_doc.get("collection_name")
    new_col = collection_name_for(new_name)
    try:
        tenant_db.create_collection(new_col)
    except CollectionInvalid:
        return 409, {"error": "target collection already exists"}
    old_coll = tenant_db[old_col]
    new_coll = tenant_db[new_col]
    docs = list(old_coll.find({}))
    if docs:
        new_coll.insert_many(docs)
    old_coll.drop()
    orgs.update_one({"_id": org_id}, {"$set": {"name": new_name, "collection_name": new_col}})
    updated = orgs.find_one({"_id": org_id})
    return 200, {"message": "organization updated", "organization": serialize_org(updated)}

def delete_org(name: str, claims: dict):
    if not claims:
        return 401, {"error": "authorization required"}
    doc = orgs.find_one({"name": name})
    if not doc:
        return 404, {"error": "organization not found"}
    if str(doc.get("_id")) != claims.get("org_id"):
        return 403, {"error": "forbidden"}
    col = doc.get("collection_name")
    tenant_db[col].drop()
    orgs.delete_one({"_id": doc.get("_id")})
    admins.delete_many({"org_id": doc.get("_id")})
    return 200, {"message": "organization deleted"}

