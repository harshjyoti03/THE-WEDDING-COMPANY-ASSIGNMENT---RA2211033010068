from flask import Flask, request, jsonify, render_template
from config.settings import MONGO_URI, MASTER_DB_NAME, TENANT_DB_NAME
from controllers.org_controller import org_bp
from controllers.auth_controller import auth_bp
from pymongo import MongoClient, ASCENDING
from pymongo.errors import CollectionInvalid
from bson.objectid import ObjectId
import os
import re
import time
import jwt
import bcrypt

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MASTER_DB_NAME = os.environ.get("MASTER_DB_NAME", "master_db")
TENANT_DB_NAME = os.environ.get("TENANT_DB_NAME", "tenant_db")
JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret")

client = MongoClient(MONGO_URI)
master_db = client[MASTER_DB_NAME]
tenant_db = client[TENANT_DB_NAME]
orgs = master_db["organizations"]
admins = master_db["admins"]

app.register_blueprint(org_bp)
app.register_blueprint(auth_bp)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET"])
def page_create():
    return render_template("create.html")

@app.route("/login", methods=["GET"])
def page_login():
    return render_template("login.html")

@app.route("/dashboard", methods=["GET"])
def page_dashboard():
    return render_template("dashboard.html")

def _redact_uri(uri: str) -> str:
    return re.sub(r"//[^/@:]+(?::[^/@]+)?@", "//****:****@", uri)

@app.route("/debug/env", methods=["GET"])
def debug_env():
    return jsonify({"mongo_uri": _redact_uri(MONGO_URI), "master_db": MASTER_DB_NAME, "tenant_db": TENANT_DB_NAME}), 200

@app.route("/debug/orgs", methods=["GET"])
def debug_orgs():
    items = [serialize_org(doc) for doc in orgs.find({}).limit(50)]
    return jsonify({"organizations": items}), 200

@app.route("/org/create", methods=["POST"])
def _deprecated_create():
    return jsonify({"error": "moved", "use": "/org/create via controller"}), 410

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))

