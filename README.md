# THE WEDDING COMPANY ASSIGNMENT

A **Multi-Tenant Organization Management Service** built using **Flask and MongoDB** with secure **JWT-based authentication**.  
This project demonstrates a scalable backend architecture where **global metadata** is stored centrally while **organization-specific data** is isolated per tenant.

---

## 👨‍💻 Project Details

**Developed By:** Harsh  
**Registration Number:** RA2211033010068  
**Email ID:** hz0620@srmist.edu.in  

---

## 🚀 Features

- Multi-tenant backend architecture
- Master database for global metadata
- Tenant database with dynamic collections per organization
- Organization lifecycle management
  - Create organization
  - Get organization details
  - Rename organization with data migration
  - Delete organization and tenant data
- Secure admin authentication
  - bcrypt password hashing
  - JWT-based authentication
- Minimal frontend using Flask templates
- Protected dashboard using JWT

---

## 🧱 System Architecture

MongoDB
│
├── master_db
│ ├── organizations
│ └── admins
│
└── tenant_db
├── org_company_a
├── org_company_b
└── org_company_c

- **Master Database:** Stores organizations and admin credentials  
- **Tenant Database:** Stores isolated data per organization  

---

## 🛠️ Technology Stack

- Backend: Flask (Python 3.10+)
- Database: MongoDB (Local or Atlas)
- Authentication: JWT (PyJWT)
- Security: bcrypt
- Frontend: HTML, CSS, JavaScript
- Environment Config: python-dotenv

---

## 📦 Setup Instructions

### 1. Install Dependencies

```bash
pip install flask pymongo bcrypt pyjwt python-dotenv

2. Environment Variables

Create a .env file in the root directory (no spaces around =):

MONGO_URI=mongodb+srv://<user>:<password>@<cluster-host>/?retryWrites=true&w=majority
MASTER_DB_NAME=master_db
TENANT_DB_NAME=tenant_db
JWT_SECRET=<strong-secret>


For local MongoDB:

MONGO_URI=mongodb://localhost:27017


⚠️ Do not commit the .env file to version control.

3. Run the Application
python app.py


Application runs at:

http://127.0.0.1:5000/

🌐 Frontend Pages
Page	Route
Home	/
Create Organization	/create
Admin Login	/login
Dashboard (Protected)	/dashboard

JWT is stored in browser localStorage after login.

🔌 API Endpoints
Create Organization

POST /org/create

{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securePassword"
}


Creates:

Organization record

Admin account

Tenant collection org_acme_corp

Get Organization

GET /org/get?organization_name=Acme Corp

Returns organization metadata from the Master Database.

Update Organization (Rename)

PUT /org/update

{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securePassword"
}


Authenticates admin

Migrates tenant data to new collection name

Delete Organization

DELETE /org/delete

Header

Authorization: Bearer <JWT>


Body

{
  "organization_name": "Acme Corp"
}


Deletes:

Tenant collection

Organization record

Admin record

Admin Login

POST /admin/login

{
  "email": "admin@acme.com",
  "password": "securePassword"
}


Returns JWT containing admin_id and org_id.

🧪 Debug Endpoints (Development)
Endpoint	Purpose
/debug/env	Verify environment variables and DB
/debug/orgs	List all organizations
🗂️ Project Structure
├── app.py
├── .env
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── create.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   ├── style.css
│   ├── common.js
│   ├── create.js
│   ├── login.js
│   └── dashboard.js
└── README.md

🧠 Common Issues

.env not loading → Restart server and ensure proper format

Wrong MongoDB cluster → Check /debug/env

Organization already exists → Remove stale records from Master DB

Tenant data missing → Verify correct MongoDB instance

🚀 Production Notes

Use Waitress or Gunicorn instead of Flask dev server

Enforce HTTPS

Use secure JWT storage (HTTP-only cookies preferred)

Implement token expiry and refresh

Add schema validation and rate limiting

📌 Future Enhancements

Role-based access control

User management per organization

Docker support

CI/CD integration

API versioning

📄 License

This project is developed for academic, learning, and assignment submission purposes.

© 2025 — Harsh
RA2211033010068
hz0620@srmist.edu.in


---

If you want, I can also:
- ✅ Make it **college-submission formatted**
- ✅ Add **architecture diagram**
- ✅ Add **screenshots section**
- ✅ Compress it for **GitHub / ATS review**

Just say the word 🚀