 ============================================================
# THE WEDDING COMPANY – Backend Assignment
 ============================================================

A Multi-Tenant Organization Management Service built using
Flask and MongoDB with secure JWT-based authentication.

Architecture Overview:
- Global metadata is stored in a Master Database
- Organization-specific data is isolated per tenant


-----------------------------
Project Details
-----------------------------
- Developed By        : Harsh
- Registration Number : RA2211033010068
- Email ID            : hz0620@srmist.edu.in


-----------------------------
Features
-----------------------------
- Multi-tenant backend architecture
- Master database for global metadata
- Tenant database with dynamic collections per organization
- Organization lifecycle management:
  - Create organization
  - Fetch organization details
  - Rename organization with tenant data migration
  - Delete organization and tenant data
- Secure admin authentication
  - bcrypt password hashing
  - JWT-based authentication
- Minimal frontend using Flask templates
- JWT-protected admin dashboard


-----------------------------
System Architecture
-----------------------------

MongoDB
|
|-- master_db
|   |-- organizations
|   |-- admins
|
|-- tenant_db
    |-- org_company_a
    |-- org_company_b
    |-- org_company_c

Master Database:
- Stores organizations metadata
- Stores admin credentials

Tenant Database:
- Stores isolated organization data per tenant


-----------------------------
Technology Stack
-----------------------------
Backend        : Flask (Python 3.10+)
Database       : MongoDB (Local / MongoDB Atlas)
Authentication : JWT (PyJWT)
Security       : bcrypt
Frontend       : HTML, CSS, JavaScript
Configuration  : python-dotenv


-----------------------------
Setup Instructions
-----------------------------

Step 1: Install Dependencies
pip install flask pymongo bcrypt pyjwt python-dotenv


Step 2: Environment Variables
Create a .env file in the root directory
(Do NOT add spaces around '=')

MongoDB Atlas
MONGO_URI=mongodb+srv://<user>:<password>@<cluster-host>/?retryWrites=true&w=majority
MASTER_DB_NAME=master_db
TENANT_DB_NAME=tenant_db
JWT_SECRET=<strong-secret>

For Local MongoDB
MONGO_URI=mongodb://localhost:27017

WARNING:
Do NOT commit the .env file to version control


Step 3: Run the Application
python app.py

Application URL
http://127.0.0.1:5000/


-----------------------------
Frontend Routes
-----------------------------
Home                  : /
Create Organization   : /create
Admin Login           : /login
Dashboard (Protected) : /dashboard

Note:
JWT is stored in browser localStorage after login


-----------------------------
API Endpoints
-----------------------------

Create Organization
POST /org/create
Request Body:
{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securePassword"
}

Creates:
- Organization record
- Admin account
- Tenant collection: org_acme_corp


Get Organization
GET /org/get?organization_name=Acme Corp

Returns organization metadata from Master Database


Update Organization (Rename)
PUT /org/update
Request Body:
{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securePassword"
}

- Authenticates admin
- Migrates tenant data to new collection name


Delete Organization
DELETE /org/delete

Header:
Authorization: Bearer <JWT>

Body:
{
  "organization_name": "Acme Corp"
}

Deletes:
- Tenant collection
- Organization record
- Admin record


Admin Login
POST /admin/login
Request Body:
{
  "email": "admin@acme.com",
  "password": "securePassword"
}

Returns JWT containing:
- admin_id
- org_id


-----------------------------
Debug Endpoints (Development)
-----------------------------
/debug/env   -> Verify environment variables and DB connection
/debug/orgs  -> List all organizations


-----------------------------
Project Structure
-----------------------------

.
|-- app.py
|-- .env
|-- templates/
|   |-- layout.html
|   |-- index.html
|   |-- create.html
|   |-- login.html
|   |-- dashboard.html
|
|-- static/
|   |-- style.css
|   |-- common.js
|   |-- create.js
|   |-- login.js
|   |-- dashboard.js
|
|-- README.md


-----------------------------
Common Issues
-----------------------------
- .env not loading
  -> Restart server and verify file format

- Wrong MongoDB cluster
  -> Check /debug/env

- Organization already exists
  -> Remove stale records from master_db

- Tenant data missing
  -> Verify correct MongoDB instance


-----------------------------
Production Notes
-----------------------------
- Use Gunicorn or Waitress instead of Flask dev server
- Enforce HTTPS
- Store JWT securely (HTTP-only cookies preferred)
- Implement token expiry and refresh
- Add schema validation and rate limiting


-----------------------------
Future Enhancements
-----------------------------
- Role-based access control (RBAC)
- User management per organization
- Docker support
- CI/CD integration
- API versioning


-----------------------------
License
-----------------------------
This project is developed for academic and learning purposes.

© 2025 — Harsh
RA2211033010068
hz0620@srmist.edu.in
