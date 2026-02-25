from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse, AssignRoomSchema, CheckoutSchema
from app.repositories.tenant_repository import TenantRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.user_repository import UserRepository
from app.usecases.tenant_usecase import (
    CreateTenantUseCase,
    GetTenantUseCase,
    GetMyTenantProfileUseCase,
    GetAllTenantsUseCase,
    GetTenantsByRoomUseCase,
    UpdateTenantUseCase,
    AssignRoomUseCase,
    CheckoutTenantUseCase,
    DeleteTenantUseCase
)
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/tenants", tags=["Tenants"])


def get_tenant_repo(db: Session = Depends(get_db)) -> TenantRepository:
    return TenantRepository(db)

def get_room_repo(db: Session = Depends(get_db)) -> RoomRepository:
    return RoomRepository(db)

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(
    data: TenantCreate,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    room_repo: RoomRepository = Depends(get_room_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new tenant (admin only).
    Set create_login=true with username & password to also create a login account for the tenant.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = CreateTenantUseCase(tenant_repo, room_repo, user_repo).execute(data)
    return _to_response(entity)


@router.get("/me", response_model=TenantResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    tenant_repo: TenantRepository = Depends(get_tenant_repo)
):
    """Tenant views their own profile using their login token."""
    entity = GetMyTenantProfileUseCase(tenant_repo).execute(current_user.id)
    return _to_response(entity)


@router.get("/", response_model=List[TenantResponse])
def get_all_tenants(
    active_only: bool = False,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    current_user: User = Depends(get_current_user)
):
    """Get all tenants (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    tenants = GetAllTenantsUseCase(tenant_repo).execute(active_only=active_only)
    return [_to_response(t) for t in tenants]


@router.get("/by-room/{room_id}", response_model=List[TenantResponse])
def get_tenants_by_room(
    room_id: int,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    current_user: User = Depends(get_current_user)
):
    """Get active tenants in a specific room (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    tenants = GetTenantsByRoomUseCase(tenant_repo).execute(room_id)
    return [_to_response(t) for t in tenants]


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    current_user: User = Depends(get_current_user)
):
    """Get a tenant by ID (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = GetTenantUseCase(tenant_repo).execute(tenant_id)
    return _to_response(entity)


@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    data: TenantUpdate,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    current_user: User = Depends(get_current_user)
):
    """Update tenant details (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = UpdateTenantUseCase(tenant_repo).execute(tenant_id, data)
    return _to_response(entity)


@router.post("/{tenant_id}/assign-room", response_model=TenantResponse)
def assign_room(
    tenant_id: int,
    data: AssignRoomSchema,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    room_repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Assign or change a tenant's room (admin only). Automatically updates room status."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = AssignRoomUseCase(tenant_repo, room_repo).execute(tenant_id, data)
    return _to_response(entity)


@router.post("/{tenant_id}/checkout", response_model=TenantResponse)
def checkout_tenant(
    tenant_id: int,
    data: CheckoutSchema,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    room_repo: RoomRepository = Depends(get_room_repo),
    current_user: User = Depends(get_current_user)
):
    """Check out a tenant. Automatically marks their room as vacant (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    entity = CheckoutTenantUseCase(tenant_repo, room_repo).execute(tenant_id, data)
    return _to_response(entity)


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(
    tenant_id: int,
    tenant_repo: TenantRepository = Depends(get_tenant_repo),
    current_user: User = Depends(get_current_user)
):
    """Delete a tenant record (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    DeleteTenantUseCase(tenant_repo).execute(tenant_id)


def _to_response(entity) -> TenantResponse:
    return TenantResponse(
        id=entity.id,
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
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )
