from typing import Optional, List
from sqlalchemy.orm import Session
from app.entities.room import RoomEntity
from app.models.room import Room
from app.repositories.interfaces.room_repository_interface import IRoomRepository


class RoomRepository(IRoomRepository):
    """Room Repository - Kitchen Equipment (SQLAlchemy implementation)."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: Room) -> RoomEntity:
        return RoomEntity(
            id=model.id,
            room_number=model.room_number,
            building_id=model.building_id,
            floor=model.floor,
            room_type=model.room_type,
            capacity=model.capacity,
            rent_amount=model.rent_amount,
            status=model.status,
            amenities=model.amenities,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: RoomEntity) -> Room:
        return Room(
            room_number=entity.room_number,
            building_id=entity.building_id,
            floor=entity.floor,
            room_type=entity.room_type,
            capacity=entity.capacity,
            rent_amount=entity.rent_amount,
            status=entity.status,
            amenities=entity.amenities,
            description=entity.description,
            is_active=entity.is_active
        )

    def create(self, room: RoomEntity) -> RoomEntity:
        db_room = self._to_model(room)
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return self._to_entity(db_room)

    def get_by_id(self, room_id: int) -> Optional[RoomEntity]:
        room = self.db.query(Room).filter(Room.id == room_id).first()
        return self._to_entity(room) if room else None

    def get_all(self, active_only: bool = False) -> List[RoomEntity]:
        query = self.db.query(Room)
        if active_only:
            query = query.filter(Room.is_active == True)
        return [self._to_entity(r) for r in query.all()]

    def get_by_building(self, building_id: int) -> List[RoomEntity]:
        rooms = self.db.query(Room).filter(Room.building_id == building_id).all()
        return [self._to_entity(r) for r in rooms]

    def get_vacant_rooms(self, building_id: Optional[int] = None) -> List[RoomEntity]:
        query = self.db.query(Room).filter(Room.status == "vacant", Room.is_active == True)
        if building_id:
            query = query.filter(Room.building_id == building_id)
        return [self._to_entity(r) for r in query.all()]

    def update(self, room: RoomEntity) -> RoomEntity:
        db_room = self.db.query(Room).filter(Room.id == room.id).first()
        if not db_room:
            raise ValueError(f"Room with id {room.id} not found")
        db_room.room_number = room.room_number
        db_room.floor = room.floor
        db_room.room_type = room.room_type
        db_room.capacity = room.capacity
        db_room.rent_amount = room.rent_amount
        db_room.status = room.status
        db_room.amenities = room.amenities
        db_room.description = room.description
        db_room.is_active = room.is_active
        self.db.commit()
        self.db.refresh(db_room)
        return self._to_entity(db_room)

    def delete(self, room_id: int) -> bool:
        room = self.db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return False
        self.db.delete(room)
        self.db.commit()
        return True
