from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.repositories.room_repository import RoomRepository
from app.repositories.building_repository import BuildingRepository
from app.usecases.room_usecase import (
    CreateRoomUseCase,
    GetRoomUseCase,
    GetAllRoomsUseCase,
    GetRoomsByBuildingUseCase,
    GetVacantRoomsUseCase,
    UpdateRoomUseCase,
    DeleteRoomUseCase
)
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])


def get_room_repo(db: Session = Depends(get_db)) -> RoomRepository:
    return RoomRepository(db)


def get_building_repo(db: Session = Depends(get_db)) -> BuildingRepository:
    return BuildingRepository(db)


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    data: RoomCreate,
    room_repo: RoomRepository = Depends(get_room_repo),
    building_repo: BuildingRepository = Depends(get_building_repo),
    current_user: User = Depends(get_current_user)
):
    """Create a new room inside a building (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = CreateRoomUseCase(room_repo, building_repo).execute(data)
    return _to_response(entity)


@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(
    active_only: bool = False,
    repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all rooms. Pass ?active_only=true to filter active ones."""
    rooms = GetAllRoomsUseCase(repo).execute(active_only=active_only)
    return [_to_response(r) for r in rooms]


@router.get("/vacant", response_model=List[RoomResponse])
def get_vacant_rooms(
    building_id: Optional[int] = None,
    repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all vacant rooms. Optionally filter by ?building_id=<id>."""
    rooms = GetVacantRoomsUseCase(repo).execute(building_id=building_id)
    return [_to_response(r) for r in rooms]


@router.get("/by-building/{building_id}", response_model=List[RoomResponse])
def get_rooms_by_building(
    building_id: int,
    repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all rooms for a specific building."""
    rooms = GetRoomsByBuildingUseCase(repo).execute(building_id)
    return [_to_response(r) for r in rooms]


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: int,
    repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Get a room by ID."""
    entity = GetRoomUseCase(repo).execute(room_id)
    return _to_response(entity)


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    data: RoomUpdate,
    repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Update a room (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = UpdateRoomUseCase(repo).execute(room_id, data)
    return _to_response(entity)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Delete a room (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    DeleteRoomUseCase(repo).execute(room_id)


def _to_response(entity) -> RoomResponse:
    return RoomResponse(
        id=entity.id,
        room_number=entity.room_number,
        building_id=entity.building_id,
        floor=entity.floor,
        room_type=entity.room_type,
        capacity=entity.capacity,
        rent_amount=entity.rent_amount,
        status=entity.status,
        amenities=entity.amenities,
        description=entity.description,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )
