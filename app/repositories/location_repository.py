from typing import Optional, List
from sqlalchemy.orm import Session
from app.entities.location import LocationEntity
from app.models.location import Location
from app.repositories.interfaces.location_repository_interface import ILocationRepository


class LocationRepository(ILocationRepository):
    """Location Repository - Kitchen Equipment (SQLAlchemy implementation)."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: Location) -> LocationEntity:
        return LocationEntity(
            id=model.id,
            name=model.name,
            address=model.address,
            city=model.city,
            state=model.state,
            pincode=model.pincode,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: LocationEntity) -> Location:
        return Location(
            id=entity.id,
            name=entity.name,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            pincode=entity.pincode,
            is_active=entity.is_active
        )

    def create(self, location: LocationEntity) -> LocationEntity:
        db_location = self._to_model(location)
        db_location.id = None  # Let DB auto-assign
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return self._to_entity(db_location)

    def get_by_id(self, location_id: int) -> Optional[LocationEntity]:
        location = self.db.query(Location).filter(Location.id == location_id).first()
        return self._to_entity(location) if location else None

    def get_all(self, active_only: bool = False) -> List[LocationEntity]:
        query = self.db.query(Location)
        if active_only:
            query = query.filter(Location.is_active == True)
        return [self._to_entity(loc) for loc in query.all()]

    def update(self, location: LocationEntity) -> LocationEntity:
        db_location = self.db.query(Location).filter(Location.id == location.id).first()
        if not db_location:
            raise ValueError(f"Location with id {location.id} not found")
        db_location.name = location.name
        db_location.address = location.address
        db_location.city = location.city
        db_location.state = location.state
        db_location.pincode = location.pincode
        db_location.is_active = location.is_active
        self.db.commit()
        self.db.refresh(db_location)
        return self._to_entity(db_location)

    def delete(self, location_id: int) -> bool:
        location = self.db.query(Location).filter(Location.id == location_id).first()
        if not location:
            return False
        self.db.delete(location)
        self.db.commit()
        return True
