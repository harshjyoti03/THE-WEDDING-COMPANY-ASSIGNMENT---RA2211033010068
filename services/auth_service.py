from config.database import admins, orgs
from utils.password_helper import check_password
from utils.jwt_helper import create_token
from models.organization_model import serialize_org

def admin_login(email: str, password: str):
    admin_doc = admins.find_one({"email": email})
    if not admin_doc:
        return 401, {"error": "invalid credentials"}
    if not check_password(password, admin_doc.get("password_hash")):
        return 401, {"error": "invalid credentials"}
    token = create_token(admin_doc.get("_id"), admin_doc.get("org_id"))
    org_doc = orgs.find_one({"_id": admin_doc.get("org_id")})
    return 200, {"token": token, "organization": serialize_org(org_doc)}

