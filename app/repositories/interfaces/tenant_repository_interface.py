from abc import ABC, abstractmethod
from typing import Optional, List
from app.entities.tenant import TenantEntity


class ITenantRepository(ABC):
    """Tenant Repository Interface - Recipe Card."""

    @abstractmethod
    def create(self, tenant: TenantEntity) -> TenantEntity:
        pass

    @abstractmethod
    def get_by_id(self, tenant_id: int) -> Optional[TenantEntity]:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[TenantEntity]:
        pass

    @abstractmethod
    def get_by_room_id(self, room_id: int) -> List[TenantEntity]:
        pass

    @abstractmethod
    def get_all(self, active_only: bool = False) -> List[TenantEntity]:
        pass

    @abstractmethod
    def update(self, tenant: TenantEntity) -> TenantEntity:
        pass

    @abstractmethod
    def delete(self, tenant_id: int) -> bool:
        pass
