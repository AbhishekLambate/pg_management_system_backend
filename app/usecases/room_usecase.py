from typing import Optional, List
from fastapi import HTTPException, status
from app.entities.room import RoomEntity
from app.repositories.interfaces.room_repository_interface import IRoomRepository
from app.repositories.interfaces.building_repository_interface import IBuildingRepository


class CreateRoomUseCase:
    def __init__(self, room_repo: IRoomRepository, building_repo: IBuildingRepository):
        self.room_repo = room_repo
        self.building_repo = building_repo

    def execute(self, data) -> RoomEntity:
        # Validate building exists
        building = self.building_repo.get_by_id(data.building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
        if not building.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Building is inactive")

        entity = RoomEntity(
            room_number=data.room_number,
            building_id=data.building_id,
            floor=data.floor,
            room_type=data.room_type,
            capacity=data.capacity,
            rent_amount=data.rent_amount,
            status="vacant",
            amenities=data.amenities,
            description=data.description,
            is_active=True
        )
        return self.room_repo.create(entity)


class GetRoomUseCase:
    def __init__(self, repo: IRoomRepository):
        self.repo = repo

    def execute(self, room_id: int) -> RoomEntity:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return room


class GetAllRoomsUseCase:
    def __init__(self, repo: IRoomRepository):
        self.repo = repo

    def execute(self, active_only: bool = False) -> List[RoomEntity]:
        return self.repo.get_all(active_only=active_only)


class GetRoomsByBuildingUseCase:
    def __init__(self, repo: IRoomRepository):
        self.repo = repo

    def execute(self, building_id: int) -> List[RoomEntity]:
        return self.repo.get_by_building(building_id)


class GetVacantRoomsUseCase:
    def __init__(self, repo: IRoomRepository):
        self.repo = repo

    def execute(self, building_id: Optional[int] = None) -> List[RoomEntity]:
        return self.repo.get_vacant_rooms(building_id=building_id)


class UpdateRoomUseCase:
    def __init__(self, repo: IRoomRepository):
        self.repo = repo

    def execute(self, room_id: int, update_data) -> RoomEntity:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if update_data.room_number is not None:
            room.room_number = update_data.room_number
        if update_data.floor is not None:
            room.floor = update_data.floor
        if update_data.room_type is not None:
            room.room_type = update_data.room_type
        if update_data.capacity is not None:
            room.capacity = update_data.capacity
        if update_data.rent_amount is not None:
            room.rent_amount = update_data.rent_amount
        if update_data.status is not None:
            room.status = update_data.status
        if update_data.amenities is not None:
            room.amenities = update_data.amenities
        if update_data.description is not None:
            room.description = update_data.description
        if update_data.is_active is not None:
            room.is_active = update_data.is_active
        return self.repo.update(room)


class DeleteRoomUseCase:
    def __init__(self, repo: IRoomRepository):
        self.repo = repo

    def execute(self, room_id: int) -> bool:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return self.repo.delete(room_id)
