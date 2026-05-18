from abc import ABC, abstractmethod
from typing import Optional, List
from app.entities.user import UserEntity


class IUserRepository(ABC):
    """
    Interface for User repository - Recipe Card (defines what tools are needed).
    
    This is like a recipe card that tells the Chef (UseCase) what kitchen equipment
    (Repository) methods are available to work with ingredients (Entities).
    The Chef doesn't need to know HOW the equipment works, just WHAT it can do.
    """
    
    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        """Create a new user."""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get user by username."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[UserEntity]:
        """Get all users."""
        pass
    
    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        """Update user."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        pass

