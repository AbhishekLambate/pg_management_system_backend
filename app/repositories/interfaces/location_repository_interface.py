from abc import ABC, abstractmethod
from typing import Optional, List
from app.entities.location import LocationEntity


class ILocationRepository(ABC):
    """
    Location Repository Interface - Recipe Card.

    Defines the contract for location data access operations.
    """

    @abstractmethod
    def create(self, location: LocationEntity) -> LocationEntity:
        pass

    @abstractmethod
    def get_by_id(self, location_id: int) -> Optional[LocationEntity]:
        pass

    @abstractmethod
    def get_all(self, active_only: bool = False) -> List[LocationEntity]:
        pass

    @abstractmethod
    def update(self, location: LocationEntity) -> LocationEntity:
        pass

    @abstractmethod
    def delete(self, location_id: int) -> bool:
        pass
