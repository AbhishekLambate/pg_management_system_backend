from typing import Optional, List
from sqlalchemy.orm import Session
from app.entities.user import UserEntity
from app.models.user import User
from app.repositories.interfaces.user_repository_interface import IUserRepository


class UserRepository(IUserRepository):
    """
    User Repository - Kitchen Equipment (tools to get/store ingredients).
    
    This is the actual kitchen equipment (oven, fridge, etc.) that implements
    the recipe card (IUserRepository interface). It knows HOW to store and
    retrieve ingredients (UserEntity) from the storage (database).
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_entity(self, model: User) -> UserEntity:
        """Convert SQLAlchemy model to domain entity."""
        return UserEntity(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: UserEntity) -> User:
        """Convert domain entity to SQLAlchemy model."""
        return User(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            role=entity.role,
            is_admin=entity.role == "admin",  # keep in sync with role
            is_active=entity.is_active
        )
    
    def create(self, user: UserEntity) -> UserEntity:
        """Create a new user."""
        db_user = self._to_model(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)
    
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Get user by ID."""
        user = self.db.query(User).filter(User.id == user_id).first()
        return self._to_entity(user) if user else None
    
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        """Get user by username."""
        user = self.db.query(User).filter(User.username == username).first()
        return self._to_entity(user) if user else None
    
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get user by email."""
        user = self.db.query(User).filter(User.email == email).first()
        return self._to_entity(user) if user else None
    
    def get_all(self) -> List[UserEntity]:
        """Get all users."""
        users = self.db.query(User).all()
        return [self._to_entity(user) for user in users]
    
    def update(self, user: UserEntity) -> UserEntity:
        """Update user."""
        db_user = self.db.query(User).filter(User.id == user.id).first()
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")
        
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.full_name = user.full_name
        db_user.role = user.role
        db_user.is_active = user.is_active
        
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True

