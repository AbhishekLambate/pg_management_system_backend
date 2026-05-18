from datetime import datetime
from typing import Optional


class RoomEntity:
    """
    Room Entity - Ingredients (data structures).

    Represents a room inside a Building.
    A room has a type, capacity, rent, and occupancy status.
    """

    ROOM_TYPES = ["single", "double", "triple", "pg"]
    STATUS_OPTIONS = ["vacant", "occupied", "maintenance"]

    def __init__(
        self,
        id: Optional[int] = None,
        room_number: str = "",
        building_id: int = 0,
        floor: int = 1,
        room_type: str = "single",
        capacity: int = 1,
        rent_amount: float = 0.0,
        status: str = "vacant",
        amenities: Optional[str] = None,
        description: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.room_number = room_number
        self.building_id = building_id
        self.floor = floor
        self.room_type = room_type
        self.capacity = capacity
        self.rent_amount = rent_amount
        self.status = status
        self.amenities = amenities
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def is_vacant(self) -> bool:
        return self.status == "vacant"

    @property
    def is_occupied(self) -> bool:
        return self.status == "occupied"

    def mark_occupied(self) -> None:
        self.status = "occupied"

    def mark_vacant(self) -> None:
        self.status = "vacant"

    def mark_maintenance(self) -> None:
        self.status = "maintenance"

    def is_valid(self) -> bool:
        return bool(self.room_number and self.building_id and self.rent_amount > 0)
