from datetime import datetime
from typing import Optional


class LocationEntity:
    """
    Location Entity - Ingredients (data structures).

    Represents a physical location/area where PG buildings exist.
    e.g. a city, neighbourhood, or address area.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        address: str = "",
        city: str = "",
        state: str = "",
        pincode: str = "",
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def is_valid(self) -> bool:
        """Validate location entity."""
        return bool(self.name and self.city)

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
