from fastapi import HTTPException, status
from app.entities.building import BuildingEntity
from app.repositories.interfaces.building_repository_interface import IBuildingRepository
from app.repositories.interfaces.location_repository_interface import ILocationRepository


class CreateBuildingUseCase:
    def __init__(self, building_repo: IBuildingRepository, location_repo: ILocationRepository):
        self.building_repo = building_repo
        self.location_repo = location_repo

    def execute(self, data) -> BuildingEntity:
        # Validate the location exists
        location = self.location_repo.get_by_id(data.location_id)
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        if not location.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location is inactive")

        entity = BuildingEntity(
            name=data.name,
            location_id=data.location_id,
            address=data.address,
            total_floors=data.total_floors,
            description=data.description,
            is_active=True
        )
        return self.building_repo.create(entity)


class GetBuildingUseCase:
    def __init__(self, repo: IBuildingRepository):
        self.repo = repo

    def execute(self, building_id: int) -> BuildingEntity:
        building = self.repo.get_by_id(building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
        return building


class GetAllBuildingsUseCase:
    def __init__(self, repo: IBuildingRepository):
        self.repo = repo

    def execute(self, active_only: bool = False):
        return self.repo.get_all(active_only=active_only)


class GetBuildingsByLocationUseCase:
    def __init__(self, repo: IBuildingRepository):
        self.repo = repo

    def execute(self, location_id: int):
        return self.repo.get_by_location(location_id)


class UpdateBuildingUseCase:
    def __init__(self, repo: IBuildingRepository):
        self.repo = repo

    def execute(self, building_id: int, update_data) -> BuildingEntity:
        building = self.repo.get_by_id(building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
        if update_data.name is not None:
            building.name = update_data.name
        if update_data.address is not None:
            building.address = update_data.address
        if update_data.total_floors is not None:
            building.total_floors = update_data.total_floors
        if update_data.description is not None:
            building.description = update_data.description
        if update_data.is_active is not None:
            building.is_active = update_data.is_active
        return self.repo.update(building)


class DeleteBuildingUseCase:
    def __init__(self, repo: IBuildingRepository):
        self.repo = repo

    def execute(self, building_id: int) -> bool:
        building = self.repo.get_by_id(building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
        return self.repo.delete(building_id)
