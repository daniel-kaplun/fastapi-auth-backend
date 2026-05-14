# FastAPI Authentication Backend

A backend authentication API built with FastAPI, SQLAlchemy, JWT authentication, and MySQL.

This repository is a reconstructed and modernized version of an authentication backend originally developed in 2024. The project was rebuilt from preserved source material and reorganized into a cleaner production-style structure for portfolio and learning purposes. It is intended for educational and portfolio purposes. 

---

## Features

- User registration and login
- Password hashing with bcrypt
- JWT access token authentication
- Refresh token authentication flow
- MySQL database integration
- SQLAlchemy ORM
- Environment variable configuration with `.env`

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyJWT
- Passlib
- Pydantic

---

## Project Structure

```text
fastapi-auth-backend/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── services/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and return JWT tokens |
| POST | `/auth/refresh` | Issue new access token from refresh token |

---

## Running Locally

### 1. Clone Repository

```bash
git clone https://github.com/daniel-kaplun/fastapi-auth-backend.git
cd fastapi-auth-backend
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create MySQL Database

Create a local MySQL database:

```sql
CREATE DATABASE fastapi_auth;
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/fastapi_auth

SECRET_KEY=your_secret_key_here
```

---

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

FastAPI server will start locally at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Authentication Flow

1. User registers an account
2. Password is hashed before storage
3. User logs in with valid credentials
4. Server issues:
   - short-lived access token
   - long-lived refresh token
5. Refresh token can be used to request new access tokens without re-authentication

---

## Notes

This project focuses on backend authentication design and security fundamentals, including:

- token-based authentication
- password hashing
- refresh token validation
- database integration
- route/service management
