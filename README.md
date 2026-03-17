# 🚀 Multi-Tenant Backend-as-a-Service (BaaS) Platform

A production-style Backend-as-a-Service (BaaS) platform built with **FastAPI, PostgreSQL, and Docker Compose**.

This platform provides **authentication, user management, project-based API keys, and tenant isolation**, allowing applications to use backend services without rebuilding infrastructure.

---

## ✨ Highlights

* 🔐 JWT-based authentication (users)
* 🔑 API key authentication (applications)
* 🧱 Multi-tenant architecture (projects per user)
* 🔄 API key rotation support
* 🐳 Fully Dockerized (API + PostgreSQL)
* ⚙️ Environment-based configuration (.env)
* 🧠 Database readiness retry logic
* 📊 Health monitoring endpoint

---

## 💡 Why This Project?

Most applications repeatedly build:

* authentication systems
* user management
* backend infrastructure
* deployment pipelines

This project solves that by providing a **reusable backend platform**, similar to:

* Firebase
* Supabase
* Auth0

It demonstrates **real-world backend + DevOps concepts**, not just CRUD.

---

## 🧠 Architecture

```
Client / App
     ↓
FastAPI Backend (Docker)
     ↓
PostgreSQL (Docker)

Auth Flow:
- JWT → Developer access
- API Key → App access
```

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Auth:** JWT (python-jose)
* **Password Hashing:** bcrypt
* **Containerization:** Docker + Docker Compose

---

## 📦 Features

### 👤 Developer (JWT Protected)

* `POST /signup` → create account
* `POST /login` → get JWT token
* `GET /me` → current user
* `GET /projects` → list your projects
* `POST /projects` → create project
* `POST /projects/{id}/rotate-key` → rotate API key

---

### 🤖 Application (API Key Based)

* `GET /app/info` → project identity via API key

Header:

```
X-API-Key: <your_api_key>
```

---

### 🔧 Utility

* `GET /health` → system health check

---

## 🔐 Authentication Model

| Actor       | Method  | Purpose             |
| ----------- | ------- | ------------------- |
| Developer   | JWT     | Manage projects     |
| Application | API Key | Access backend APIs |

---

## ▶️ Run Locally (Docker Recommended)

### 1. Create `.env`

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/baas
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 2. Start the platform

```bash
docker compose up --build
```

---

### 3. Access API

Swagger UI:

```
http://localhost:8000/docs
```

Health check:

```
http://localhost:8000/health
```

---

## 🧪 Example Workflow

1. Signup → Login → Get JWT
2. Create project → Get API key
3. Use API key in app:

```
X-API-Key: <your_key>
```

4. Call `/app/info`

---

## 📸 API Demo


---

## 🔮 Future Improvements

* ☁️ AWS EC2 deployment
* 🔁 CI/CD with GitHub Actions
* 🔒 HTTPS with Nginx + Let’s Encrypt
* 📊 Monitoring (Prometheus + Grafana)
* ⚡ Rate limiting per project
* 📈 Usage analytics dashboard
* ☸️ Kubernetes deployment

---

## 🧾 Project Significance

This project demonstrates:

* Backend architecture design
* Multi-tenant systems
* Authentication & authorization
* API key management
* Docker-based deployment
* DevOps readiness

---

## 👨‍💻 Author

Pranav
