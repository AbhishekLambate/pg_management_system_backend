from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.repositories.building_repository import BuildingRepository
from app.repositories.location_repository import LocationRepository
from app.usecases.building_usecase import (
    CreateBuildingUseCase,
    GetBuildingUseCase,
    GetAllBuildingsUseCase,
    GetBuildingsByLocationUseCase,
    UpdateBuildingUseCase,
    DeleteBuildingUseCase
)
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/buildings", tags=["Buildings"])


def get_building_repo(db: Session = Depends(get_db)) -> BuildingRepository:
    return BuildingRepository(db)


def get_location_repo(db: Session = Depends(get_db)) -> LocationRepository:
    return LocationRepository(db)


@router.post("/", response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
def create_building(
    data: BuildingCreate,
    building_repo: BuildingRepository = Depends(get_building_repo),
    location_repo: LocationRepository = Depends(get_location_repo),
    current_user: User = Depends(get_current_user)
):
    """Create a new building under a location (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = CreateBuildingUseCase(building_repo, location_repo).execute(data)
    return _to_response(entity)


@router.get("/", response_model=List[BuildingResponse])
def get_all_buildings(
    active_only: bool = False,
    repo: BuildingRepository = Depends(get_building_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all buildings. Pass ?active_only=true to filter active ones."""
    buildings = GetAllBuildingsUseCase(repo).execute(active_only=active_only)
    return [_to_response(b) for b in buildings]


@router.get("/by-location/{location_id}", response_model=List[BuildingResponse])
def get_buildings_by_location(
    location_id: int,
    repo: BuildingRepository = Depends(get_building_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all buildings for a specific location."""
    buildings = GetBuildingsByLocationUseCase(repo).execute(location_id)
    return [_to_response(b) for b in buildings]


@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(
    building_id: int,
    repo: BuildingRepository = Depends(get_building_repo),
    current_user: User = Depends(get_current_user)
):
    """Get a building by ID."""
    entity = GetBuildingUseCase(repo).execute(building_id)
    return _to_response(entity)


@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(
    building_id: int,
    data: BuildingUpdate,
    repo: BuildingRepository = Depends(get_building_repo),
    current_user: User = Depends(get_current_user)
):
    """Update a building (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = UpdateBuildingUseCase(repo).execute(building_id, data)
    return _to_response(entity)


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(
    building_id: int,
    repo: BuildingRepository = Depends(get_building_repo),
    current_user: User = Depends(get_current_user)
):
    """Delete a building (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    DeleteBuildingUseCase(repo).execute(building_id)


def _to_response(entity) -> BuildingResponse:
    return BuildingResponse(
        id=entity.id,
        name=entity.name,
        location_id=entity.location_id,
        address=entity.address,
        total_floors=entity.total_floors,
        description=entity.description,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )
