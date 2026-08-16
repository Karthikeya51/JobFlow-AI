# JobFlow AI - Phase 1 Foundation

AI-powered job application management platform.

**Phase 1: Authentication & Project Foundation**

## Features (Phase 1)

- User registration and login
- JWT-based authentication
- Secure password hashing
- Protected API routes
- Protected frontend routes

## Tech Stack

**Frontend:**

- React 18
- Vite
- React Router
- Axios
- Bootstrap 5

**Backend:**

- Python 3.9+
- FastAPI
- MongoDB (MongoDB Atlas)
- Pydantic
- PyJWT
- bcrypt

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The `.env` file is already created with default values.

**Optional:** Update MongoDB URI in `.env` if you have MongoDB Atlas set up.

```bash
python -m pytest tests/  # Run tests
python -m uvicorn app.main:app --reload  # Run server
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

See `.env.example` files in both `backend/` and `frontend/` directories.

## Project Structure

```
jobflow-ai/
├── backend/          # FastAPI + MongoDB
├── frontend/         # React + Vite
├── .github/
│   └── workflows/    # CI/CD (Phase 2)
└── docs/
```

## API Endpoints (Phase 1)

- `GET /health` - Health check
- `POST /api/auth/register` - Register
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user (protected)

## Testing

```bash
cd backend
python -m pytest tests/ -v
```

## Next Steps (Phase 2)

- Job applications CRUD
- Dashboard
- Resume management
- AI analysis integration

---

**Last Updated:** Phase 1 Foundation
