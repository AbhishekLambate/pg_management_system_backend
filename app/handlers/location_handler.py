from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.repositories.location_repository import LocationRepository
from app.usecases.location_usecase import (
    CreateLocationUseCase,
    GetLocationUseCase,
    GetAllLocationsUseCase,
    UpdateLocationUseCase,
    DeleteLocationUseCase
)
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/locations", tags=["Locations"])


def get_location_repo(db: Session = Depends(get_db)) -> LocationRepository:
    return LocationRepository(db)


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    data: LocationCreate,
    repo: LocationRepository = Depends(get_location_repo),
    current_user: User = Depends(get_current_user)
):
    """Create a new location (admin only)."""
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = CreateLocationUseCase(repo).execute(data)
    return _to_response(entity)


@router.get("/", response_model=List[LocationResponse])
def get_all_locations(
    active_only: bool = False,
    repo: LocationRepository = Depends(get_location_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all locations. Pass ?active_only=true to filter active ones."""
    locations = GetAllLocationsUseCase(repo).execute(active_only=active_only)
    return [_to_response(loc) for loc in locations]


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repo),
    current_user: User = Depends(get_current_user)
):
    """Get a location by ID."""
    entity = GetLocationUseCase(repo).execute(location_id)
    return _to_response(entity)


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    data: LocationUpdate,
    repo: LocationRepository = Depends(get_location_repo),
    current_user: User = Depends(get_current_user)
):
    """Update a location (admin only)."""
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = UpdateLocationUseCase(repo).execute(location_id, data)
    return _to_response(entity)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location_id: int,
    repo: LocationRepository = Depends(get_location_repo),
    current_user: User = Depends(get_current_user)
):
    """Delete a location (admin only). Also deletes all buildings in it."""
    if not current_user.is_admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    DeleteLocationUseCase(repo).execute(location_id)


def _to_response(entity) -> LocationResponse:
    return LocationResponse(
        id=entity.id,
        name=entity.name,
        address=entity.address,
        city=entity.city,
        state=entity.state,
        pincode=entity.pincode,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )
