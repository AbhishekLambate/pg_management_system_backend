from datetime import date
from typing import List, Optional
from fastapi import HTTPException, status
from app.entities.tenant import TenantEntity
from app.repositories.interfaces.tenant_repository_interface import ITenantRepository
from app.repositories.interfaces.room_repository_interface import IRoomRepository
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.utils.security import get_password_hash


class CreateTenantUseCase:
    def __init__(self, tenant_repo: ITenantRepository, room_repo: IRoomRepository, user_repo: IUserRepository):
        self.tenant_repo = tenant_repo
        self.room_repo = room_repo
        self.user_repo = user_repo

    def execute(self, data) -> TenantEntity:
        # Validate room if provided
        if data.room_id:
            room = self.room_repo.get_by_id(data.room_id)
            if not room:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
            if room.status != "vacant":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room is not vacant")

        # Optionally create a login user account
        user_id = None
        if data.create_login:
            if not data.username or not data.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="username and password are required when create_login=True"
                )
            # Check username doesn't already exist
            existing = self.user_repo.get_by_username(data.username)
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

            from app.entities.user import UserEntity
            user_entity = UserEntity(
                username=data.username,
                email=data.email or f"{data.username}@pg.local",
                hashed_password=get_password_hash(data.password),
                full_name=f"{data.first_name} {data.last_name}",
                role="user",
                is_active=True
            )
            created_user = self.user_repo.create(user_entity)
            user_id = created_user.id

        # Build tenant entity
        tenant = TenantEntity(
            user_id=user_id,
            room_id=data.room_id,
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            alternate_phone=data.alternate_phone,
            email=data.email,
            permanent_address=data.permanent_address,
            emergency_contact_name=data.emergency_contact_name,
            emergency_contact_phone=data.emergency_contact_phone,
            id_proof_type=data.id_proof_type,
            id_proof_number=data.id_proof_number,
            move_in_date=data.move_in_date,
            deposit_amount=data.deposit_amount,
            status="active",
            is_active=True
        )
        created_tenant = self.tenant_repo.create(tenant)

        # Mark room as occupied
        if data.room_id:
            room = self.room_repo.get_by_id(data.room_id)
            room.mark_occupied()
            self.room_repo.update(room)

        return created_tenant


class GetTenantUseCase:
    def __init__(self, repo: ITenantRepository):
        self.repo = repo

    def execute(self, tenant_id: int) -> TenantEntity:
        tenant = self.repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        return tenant


class GetMyTenantProfileUseCase:
    """For tenants to view their own profile using their user_id."""
    def __init__(self, repo: ITenantRepository):
        self.repo = repo

    def execute(self, user_id: int) -> TenantEntity:
        tenant = self.repo.get_by_user_id(user_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tenant profile linked to your account")
        return tenant


class GetAllTenantsUseCase:
    def __init__(self, repo: ITenantRepository):
        self.repo = repo

    def execute(self, active_only: bool = False) -> List[TenantEntity]:
        return self.repo.get_all(active_only=active_only)


class GetTenantsByRoomUseCase:
    def __init__(self, repo: ITenantRepository):
        self.repo = repo

    def execute(self, room_id: int) -> List[TenantEntity]:
        return self.repo.get_by_room_id(room_id)


class UpdateTenantUseCase:
    def __init__(self, repo: ITenantRepository):
        self.repo = repo

    def execute(self, tenant_id: int, data) -> TenantEntity:
        tenant = self.repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        if data.first_name is not None:
            tenant.first_name = data.first_name
        if data.last_name is not None:
            tenant.last_name = data.last_name
        if data.phone is not None:
            tenant.phone = data.phone
        if data.alternate_phone is not None:
            tenant.alternate_phone = data.alternate_phone
        if data.email is not None:
            tenant.email = data.email
        if data.permanent_address is not None:
            tenant.permanent_address = data.permanent_address
        if data.emergency_contact_name is not None:
            tenant.emergency_contact_name = data.emergency_contact_name
        if data.emergency_contact_phone is not None:
            tenant.emergency_contact_phone = data.emergency_contact_phone
        if data.id_proof_type is not None:
            tenant.id_proof_type = data.id_proof_type
        if data.id_proof_number is not None:
            tenant.id_proof_number = data.id_proof_number
        if data.deposit_amount is not None:
            tenant.deposit_amount = data.deposit_amount
        if data.status is not None:
            tenant.status = data.status
        if data.is_active is not None:
            tenant.is_active = data.is_active
        return self.repo.update(tenant)


class AssignRoomUseCase:
    def __init__(self, tenant_repo: ITenantRepository, room_repo: IRoomRepository):
        self.tenant_repo = tenant_repo
        self.room_repo = room_repo

    def execute(self, tenant_id: int, data) -> TenantEntity:
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

        room = self.room_repo.get_by_id(data.room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        if room.status != "vacant":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room is not vacant")

        # Free up old room if present
        if tenant.room_id and tenant.room_id != data.room_id:
            old_room = self.room_repo.get_by_id(tenant.room_id)
            if old_room:
                old_room.mark_vacant()
                self.room_repo.update(old_room)

        tenant.room_id = data.room_id
        if data.move_in_date:
            tenant.move_in_date = data.move_in_date
        tenant.status = "active"

        # Mark new room as occupied
        room.mark_occupied()
        self.room_repo.update(room)

        return self.tenant_repo.update(tenant)


class CheckoutTenantUseCase:
    def __init__(self, tenant_repo: ITenantRepository, room_repo: IRoomRepository):
        self.tenant_repo = tenant_repo
        self.room_repo = room_repo

    def execute(self, tenant_id: int, data) -> TenantEntity:
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        if tenant.status == "checked_out":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tenant already checked out")

        # Free the room
        if tenant.room_id:
            room = self.room_repo.get_by_id(tenant.room_id)
            if room:
                room.mark_vacant()
                self.room_repo.update(room)

        tenant.checkout(data.move_out_date)
        return self.tenant_repo.update(tenant)


class DeleteTenantUseCase:
    def __init__(self, repo: ITenantRepository):
        self.repo = repo

    def execute(self, tenant_id: int) -> bool:
        tenant = self.repo.get_by_id(tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        return self.repo.delete(tenant_id)
