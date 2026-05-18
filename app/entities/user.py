from datetime import datetime
from typing import Optional


class UserEntity:
    """
    User Entity - Ingredients (data structures).
    
    This is like raw ingredients in a restaurant. Pure data structures with
    business logic, no dependencies on how they're stored or cooked.
    The Chef (UseCase) works with these ingredients following recipes.
    """
    
    def __init__(
        self,
        id: Optional[int] = None,
        username: str = "",
        email: str = "",
        hashed_password: str = "",
        full_name: Optional[str] = None,
        role: str = "user",
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin based on role."""
        return self.role == "admin"
    
    def is_valid(self) -> bool:
        """Validate user entity."""
        return bool(self.username and self.email and self.hashed_password)
    
    def activate(self) -> None:
        """Activate user account."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
    
    def promote_to_admin(self) -> None:
        """Promote user to admin."""
        self.role = "admin"
    
    def demote_from_admin(self) -> None:
        """Remove admin privileges."""
        self.role = "user"

