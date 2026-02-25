from fastapi import HTTPException, status
from app.entities.location import LocationEntity
from app.repositories.interfaces.location_repository_interface import ILocationRepository


class CreateLocationUseCase:
    def __init__(self, repo: ILocationRepository):
        self.repo = repo

    def execute(self, data) -> LocationEntity:
        entity = LocationEntity(
            name=data.name,
            address=data.address,
            city=data.city,
            state=data.state,
            pincode=data.pincode,
            is_active=True
        )
        return self.repo.create(entity)


class GetLocationUseCase:
    def __init__(self, repo: ILocationRepository):
        self.repo = repo

    def execute(self, location_id: int) -> LocationEntity:
        location = self.repo.get_by_id(location_id)
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        return location


class GetAllLocationsUseCase:
    def __init__(self, repo: ILocationRepository):
        self.repo = repo

    def execute(self, active_only: bool = False):
        return self.repo.get_all(active_only=active_only)


class UpdateLocationUseCase:
    def __init__(self, repo: ILocationRepository):
        self.repo = repo

    def execute(self, location_id: int, update_data) -> LocationEntity:
        location = self.repo.get_by_id(location_id)
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        if update_data.name is not None:
            location.name = update_data.name
        if update_data.address is not None:
            location.address = update_data.address
        if update_data.city is not None:
            location.city = update_data.city
        if update_data.state is not None:
            location.state = update_data.state
        if update_data.pincode is not None:
            location.pincode = update_data.pincode
        if update_data.is_active is not None:
            location.is_active = update_data.is_active
        return self.repo.update(location)


class DeleteLocationUseCase:
    def __init__(self, repo: ILocationRepository):
        self.repo = repo

    def execute(self, location_id: int) -> bool:
        location = self.repo.get_by_id(location_id)
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        return self.repo.delete(location_id)
