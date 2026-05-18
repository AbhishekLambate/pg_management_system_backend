from typing import Optional, List
from sqlalchemy.orm import Session
from app.entities.building import BuildingEntity
from app.models.building import Building
from app.repositories.interfaces.building_repository_interface import IBuildingRepository


class BuildingRepository(IBuildingRepository):
    """Building Repository - Kitchen Equipment (SQLAlchemy implementation)."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: Building) -> BuildingEntity:
        return BuildingEntity(
            id=model.id,
            name=model.name,
            location_id=model.location_id,
            address=model.address,
            total_floors=model.total_floors,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: BuildingEntity) -> Building:
        return Building(
            name=entity.name,
            location_id=entity.location_id,
            address=entity.address,
            total_floors=entity.total_floors,
            description=entity.description,
            is_active=entity.is_active
        )

    def create(self, building: BuildingEntity) -> BuildingEntity:
        db_building = self._to_model(building)
        self.db.add(db_building)
        self.db.commit()
        self.db.refresh(db_building)
        return self._to_entity(db_building)

    def get_by_id(self, building_id: int) -> Optional[BuildingEntity]:
        building = self.db.query(Building).filter(Building.id == building_id).first()
        return self._to_entity(building) if building else None

    def get_all(self, active_only: bool = False) -> List[BuildingEntity]:
        query = self.db.query(Building)
        if active_only:
            query = query.filter(Building.is_active == True)
        return [self._to_entity(b) for b in query.all()]

    def get_by_location(self, location_id: int) -> List[BuildingEntity]:
        buildings = self.db.query(Building).filter(Building.location_id == location_id).all()
        return [self._to_entity(b) for b in buildings]

    def update(self, building: BuildingEntity) -> BuildingEntity:
        db_building = self.db.query(Building).filter(Building.id == building.id).first()
        if not db_building:
            raise ValueError(f"Building with id {building.id} not found")
        db_building.name = building.name
        db_building.address = building.address
        db_building.total_floors = building.total_floors
        db_building.description = building.description
        db_building.is_active = building.is_active
        self.db.commit()
        self.db.refresh(db_building)
        return self._to_entity(db_building)

    def delete(self, building_id: int) -> bool:
        building = self.db.query(Building).filter(Building.id == building_id).first()
        if not building:
            return False
        self.db.delete(building)
        self.db.commit()
        return True
