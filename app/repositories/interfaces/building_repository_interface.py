from abc import ABC, abstractmethod
from typing import Optional, List
from app.entities.building import BuildingEntity


class IBuildingRepository(ABC):
    """
    Building Repository Interface - Recipe Card.

    Defines the contract for building data access operations.
    """

    @abstractmethod
    def create(self, building: BuildingEntity) -> BuildingEntity:
        pass

    @abstractmethod
    def get_by_id(self, building_id: int) -> Optional[BuildingEntity]:
        pass

    @abstractmethod
    def get_all(self, active_only: bool = False) -> List[BuildingEntity]:
        pass

    @abstractmethod
    def get_by_location(self, location_id: int) -> List[BuildingEntity]:
        pass

    @abstractmethod
    def update(self, building: BuildingEntity) -> BuildingEntity:
        pass

    @abstractmethod
    def delete(self, building_id: int) -> bool:
        pass
