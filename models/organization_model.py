import re

def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

def collection_name_for(name: str) -> str:
    return f"org_{slugify(name)}"

def serialize_org(doc: dict) -> dict:
    return {
        "organization_id": str(doc.get("_id")),
        "organization_name": doc.get("name"),
        "collection_name": doc.get("collection_name"),
        "connection": doc.get("connection"),
        "admin_id": str(doc.get("admin_id")) if doc.get("admin_id") else None,
    }

