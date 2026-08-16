from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.connection import get_database
from app.routers import analysis_router, applications_router, auth_router, dashboard_router, resume_router

app = FastAPI(
    title="JobFlow AI API",
    description="AI-powered job application management platform",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(applications_router)
app.include_router(dashboard_router)
app.include_router(resume_router)
app.include_router(analysis_router)

# Create application indexes on startup
@app.on_event("startup")
async def startup_event():
    db = get_database()
    db["applications"].create_index("user_id")
    db["applications"].create_index([("user_id", 1), ("status", 1)])
    db["applications"].create_index([("user_id", 1), ("created_at", -1)])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "jobflow-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
