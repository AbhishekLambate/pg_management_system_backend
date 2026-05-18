from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.models.tenant import Tenant
from app.models.room import Room
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard statistics
    """
    # Total Capacity
    total_capacity = db.query(func.sum(Room.capacity)).scalar() or 0

    # Active Tenants
    active_tenants = db.query(Tenant).filter(Tenant.status == "active").count()

    # Available beds
    available_beds = total_capacity - active_tenants
    if available_beds < 0:
        available_beds = 0

    # Monthly Revenue (Projected based on active tenants and their room rent)
    # This is a simple projection: sum of rent_amount for the room of each active tenant
    revenue_query = db.query(func.sum(Room.rent_amount)).join(Tenant, Tenant.room_id == Room.id).filter(Tenant.status == "active").scalar() or 0

    return {
        "total_capacity": total_capacity,
        "active_tenants": active_tenants,
        "available_beds": available_beds,
        "projected_revenue": revenue_query,
        "occupancy_rate": round((active_tenants / total_capacity * 100), 1) if total_capacity > 0 else 0
    }
