def serialize_admin(doc: dict) -> dict:
    return {
        "admin_id": str(doc.get("_id")),
        "email": doc.get("email"),
        "org_id": str(doc.get("org_id")) if doc.get("org_id") else None,
    }

