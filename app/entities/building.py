from datetime import datetime
from typing import Optional


class BuildingEntity:
    """
    Building Entity - Ingredients (data structures).

    Represents a physical PG building that belongs to a Location.
    A building contains multiple rooms.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        location_id: int = 0,
        address: Optional[str] = None,
        total_floors: int = 1,
        description: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.location_id = location_id
        self.address = address
        self.total_floors = total_floors
        self.description = description
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def is_valid(self) -> bool:
        """Validate building entity."""
        return bool(self.name and self.location_id)

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
