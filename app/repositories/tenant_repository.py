from typing import Optional, List
from sqlalchemy.orm import Session
from app.entities.tenant import TenantEntity
from app.models.tenant import Tenant
from app.repositories.interfaces.tenant_repository_interface import ITenantRepository


class TenantRepository(ITenantRepository):
    """Tenant Repository - Kitchen Equipment (SQLAlchemy implementation)."""

    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: Tenant) -> TenantEntity:
        return TenantEntity(
            id=model.id,
            user_id=model.user_id,
            room_id=model.room_id,
            first_name=model.first_name,
            last_name=model.last_name,
            phone=model.phone,
            alternate_phone=model.alternate_phone,
            email=model.email,
            permanent_address=model.permanent_address,
            emergency_contact_name=model.emergency_contact_name,
            emergency_contact_phone=model.emergency_contact_phone,
            id_proof_type=model.id_proof_type,
            id_proof_number=model.id_proof_number,
            move_in_date=model.move_in_date,
            move_out_date=model.move_out_date,
            deposit_amount=model.deposit_amount,
            status=model.status,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: TenantEntity) -> Tenant:
        return Tenant(
            user_id=entity.user_id,
            room_id=entity.room_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            phone=entity.phone,
            alternate_phone=entity.alternate_phone,
            email=entity.email,
            permanent_address=entity.permanent_address,
            emergency_contact_name=entity.emergency_contact_name,
            emergency_contact_phone=entity.emergency_contact_phone,
            id_proof_type=entity.id_proof_type,
            id_proof_number=entity.id_proof_number,
            move_in_date=entity.move_in_date,
            move_out_date=entity.move_out_date,
            deposit_amount=entity.deposit_amount,
            status=entity.status,
            is_active=entity.is_active
        )

    def create(self, tenant: TenantEntity) -> TenantEntity:
        db_tenant = self._to_model(tenant)
        self.db.add(db_tenant)
        self.db.commit()
        self.db.refresh(db_tenant)
        return self._to_entity(db_tenant)

    def get_by_id(self, tenant_id: int) -> Optional[TenantEntity]:
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        return self._to_entity(tenant) if tenant else None

    def get_by_user_id(self, user_id: int) -> Optional[TenantEntity]:
        tenant = self.db.query(Tenant).filter(Tenant.user_id == user_id).first()
        return self._to_entity(tenant) if tenant else None

    def get_by_room_id(self, room_id: int) -> List[TenantEntity]:
        tenants = self.db.query(Tenant).filter(
            Tenant.room_id == room_id,
            Tenant.status == "active"
        ).all()
        return [self._to_entity(t) for t in tenants]

    def get_all(self, active_only: bool = False) -> List[TenantEntity]:
        query = self.db.query(Tenant)
        if active_only:
            query = query.filter(Tenant.status == "active")
        return [self._to_entity(t) for t in query.all()]

    def update(self, tenant: TenantEntity) -> TenantEntity:
        db_tenant = self.db.query(Tenant).filter(Tenant.id == tenant.id).first()
        if not db_tenant:
            raise ValueError(f"Tenant with id {tenant.id} not found")
        db_tenant.user_id = tenant.user_id
        db_tenant.room_id = tenant.room_id
        db_tenant.first_name = tenant.first_name
        db_tenant.last_name = tenant.last_name
        db_tenant.phone = tenant.phone
        db_tenant.alternate_phone = tenant.alternate_phone
        db_tenant.email = tenant.email
        db_tenant.permanent_address = tenant.permanent_address
        db_tenant.emergency_contact_name = tenant.emergency_contact_name
        db_tenant.emergency_contact_phone = tenant.emergency_contact_phone
        db_tenant.id_proof_type = tenant.id_proof_type
        db_tenant.id_proof_number = tenant.id_proof_number
        db_tenant.move_in_date = tenant.move_in_date
        db_tenant.move_out_date = tenant.move_out_date
        db_tenant.deposit_amount = tenant.deposit_amount
        db_tenant.status = tenant.status
        db_tenant.is_active = tenant.is_active
        self.db.commit()
        self.db.refresh(db_tenant)
        return self._to_entity(db_tenant)

    def delete(self, tenant_id: int) -> bool:
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            return False
        self.db.delete(tenant)
        self.db.commit()
        return True
