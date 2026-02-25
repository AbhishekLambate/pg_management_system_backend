from abc import ABC, abstractmethod
from typing import Optional, List
from app.entities.room import RoomEntity


class IRoomRepository(ABC):
    """Room Repository Interface - Recipe Card."""

    @abstractmethod
    def create(self, room: RoomEntity) -> RoomEntity:
        pass

    @abstractmethod
    def get_by_id(self, room_id: int) -> Optional[RoomEntity]:
        pass

    @abstractmethod
    def get_all(self, active_only: bool = False) -> List[RoomEntity]:
        pass

    @abstractmethod
    def get_by_building(self, building_id: int) -> List[RoomEntity]:
        pass

    @abstractmethod
    def get_vacant_rooms(self, building_id: Optional[int] = None) -> List[RoomEntity]:
        pass

    @abstractmethod
    def update(self, room: RoomEntity) -> RoomEntity:
        pass

    @abstractmethod
    def delete(self, room_id: int) -> bool:
        pass
