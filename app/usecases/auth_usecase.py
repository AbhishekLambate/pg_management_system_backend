from typing import Optional
from fastapi import HTTPException, status
from app.entities.user import UserEntity
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.user import UserCreate
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings
from datetime import timedelta


class RegisterUserUseCase:
    """
    Register User Use Case - Chef (cooks the meal, follows recipe).
    
    The Chef receives ingredients (UserEntity) and uses kitchen equipment
    (Repository via Interface) to prepare the meal. The Chef follows the
    recipe (Interface contract) but doesn't need to know HOW the equipment works.
    """
    
    def __init__(self, user_repository: IUserRepository):
        # Chef gets the kitchen equipment (repository) that follows the recipe (interface)
        self.user_repository = user_repository
    
    def execute(self, user_data: UserCreate) -> UserEntity:
        """Execute user registration."""
        # Check if username already exists
        existing_user = self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = self.user_repository.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user entity with role from user_data
        hashed_password = get_password_hash(user_data.password)
        user_entity = UserEntity(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role,  # Use role from request
            is_active=True
        )
        
        # Save to repository
        return self.user_repository.create(user_entity)


class LoginUseCase:
    """
    Login Use Case - Chef (cooks the meal, follows recipe).
    
    The Chef authenticates users using the kitchen equipment (Repository)
    following the recipe (Interface contract).
    """
    
    def __init__(self, user_repository: IUserRepository):
        # Chef gets the kitchen equipment (repository) that follows the recipe (interface)
        self.user_repository = user_repository
    
    def execute(self, username: str, password: str) -> dict:
        """Execute user login."""
        # Get user by username
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.username,
                "role": user.role,
                "email": user.email,
                "id": user.id
            },
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }


class GetUserUseCase:
    """
    Get User Use Case - Chef (cooks the meal, follows recipe).
    
    The Chef retrieves user information using the kitchen equipment (Repository)
    following the recipe (Interface contract).
    """
    
    def __init__(self, user_repository: IUserRepository):
        # Chef gets the kitchen equipment (repository) that follows the recipe (interface)
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> UserEntity:
        """Execute get user by ID."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def execute_by_username(self, username: str) -> UserEntity:
        """Execute get user by username."""
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user


class GetAllUsersUseCase:
    """
    Get All Users Use Case - Chef (cooks the meal, follows recipe).
    
    The Chef retrieves all users using the kitchen equipment (Repository)
    following the recipe (Interface contract).
    """
    
    def __init__(self, user_repository: IUserRepository):
        # Chef gets the kitchen equipment (repository) that follows the recipe (interface)
        self.user_repository = user_repository
    
    def execute(self) -> list[UserEntity]:
        """Execute get all users."""
        return self.user_repository.get_all()


class UpdateUserUseCase:
    """
    Update User Use Case - Chef (cooks the meal, follows recipe).

    The Chef updates a user's details using the kitchen equipment (Repository)
    following the recipe (Interface contract). Only the fields provided are updated.
    """

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int, update_data) -> "UserEntity":
        """Execute update user by ID (partial update)."""
        from app.schemas.user import UserUpdate

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Apply only provided fields
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.is_active is not None:
            user.is_active = update_data.is_active
        if update_data.role is not None:
            user.role = update_data.role
        if update_data.password is not None:
            user.hashed_password = get_password_hash(update_data.password)

        return self.user_repository.update(user)


class DeleteUserUseCase:
    """
    Delete User Use Case - Chef (cooks the meal, follows recipe).

    The Chef deletes a user using the kitchen equipment (Repository)
    following the recipe (Interface contract).
    """

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> bool:
        """Execute delete user by ID."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return self.user_repository.delete(user_id)
