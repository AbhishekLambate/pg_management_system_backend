from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.handlers import auth_handler
from app.handlers import location_handler, building_handler, room_handler, tenant_handler, dashboard_handler, payment_handler, staff_handler, complaint_handler, expense_handler, visitor_handler, notice_handler
# Import models so SQLAlchemy creates all tables
from app.models import user, location, building, room, tenant  # noqa: F401

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="PG Management System API",
    description="Backend API for Paying Guest (PG) Management System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include handlers
app.include_router(auth_handler.router)
app.include_router(location_handler.router)
app.include_router(building_handler.router)
app.include_router(room_handler.router)
app.include_router(tenant_handler.router)
app.include_router(dashboard_handler.router)
app.include_router(payment_handler.router)
app.include_router(staff_handler.router)
app.include_router(complaint_handler.router)
app.include_router(expense_handler.router)
app.include_router(visitor_handler.router)
app.include_router(notice_handler.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "PG Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

