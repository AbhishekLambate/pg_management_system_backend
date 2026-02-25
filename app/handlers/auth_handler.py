from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from app.repositories.user_repository import UserRepository
from app.usecases.auth_usecase import (
    RegisterUserUseCase,
    LoginUseCase,
    GetUserUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Dependency to get user repository - Provides kitchen equipment.
    
    This provides the actual kitchen equipment (Repository implementation)
    to the Chef (UseCase). The Waiter (Handler) gets the equipment and
    gives it to the Chef to use.
    """
    return UserRepository(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    repository: UserRepository = Depends(get_user_repository)
):
    """
    Register a new user with role.
    
    Role can be 'admin' or 'user'. Default is 'user'.
    Waiter (Handler) receives the order (request), gives kitchen equipment
    (Repository) to the Chef (UseCase), Chef prepares the meal (business logic),
    Waiter serves the food (response).
    """
    # Waiter gives the kitchen equipment to the Chef
    use_case = RegisterUserUseCase(repository)
    # Chef prepares the meal (executes business logic)
    user_entity = use_case.execute(user_data)
    
    # Convert entity to response
    return UserResponse(
        id=user_entity.id,
        username=user_entity.username,
        email=user_entity.email,
        full_name=user_entity.full_name,
        role=user_entity.role,
        is_active=user_entity.is_active,
        created_at=user_entity.created_at,
        updated_at=user_entity.updated_at
    )


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    repository: UserRepository = Depends(get_user_repository)
):
    """
    Login and get JWT access token.
    
    Waiter (Handler) receives the order (login request), gives kitchen equipment
    (Repository) to the Chef (UseCase), Chef authenticates (business logic),
    Waiter serves the token (response).
    """
    # Waiter gives the kitchen equipment to the Chef
    use_case = LoginUseCase(repository)
    # Chef prepares the meal (executes authentication logic)
    result = use_case.execute(user_credentials.username, user_credentials.password)
    
    return Token(
        access_token=result["access_token"],
        token_type=result["token_type"]
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    
    Waiter (Handler) receives the order, already has the user from authentication,
    Waiter serves the user information (response).
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    current_user: User = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository)
):
    """
    Get all users (admin only).
    
    Waiter (Handler) receives the order, checks permissions, gives kitchen equipment
    (Repository) to the Chef (UseCase), Chef retrieves all users, Waiter serves the list.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all users"
        )
    
    # Waiter gives the kitchen equipment to the Chef
    use_case = GetAllUsersUseCase(repository)
    # Chef prepares the meal (executes business logic)
    users = use_case.execute()
    
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository)
):
    """
    Get a specific user by ID (admin only, or own profile).
    
    Waiter (Handler) receives the order, checks permissions, gives kitchen equipment
    (Repository) to the Chef (UseCase), Chef retrieves the user, Waiter serves the user info.
    """
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Waiter gives the kitchen equipment to the Chef
    use_case = GetUserUseCase(repository)
    # Chef prepares the meal (executes business logic)
    user_entity = use_case.execute(user_id)
    
    return UserResponse(
        id=user_entity.id,
        username=user_entity.username,
        email=user_entity.email,
        full_name=user_entity.full_name,
        role=user_entity.role,
        is_active=user_entity.is_active,
        created_at=user_entity.created_at,
        updated_at=user_entity.updated_at
    )


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository)
):
    """
    Update a user by ID.

    - Admin can update any user including their role.
    - Regular users can only update their own profile (email, full_name, password).
    - Role change is restricted to admins only.
    """
    # Non-admins can only update their own profile
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this user"
        )

    # Only admins can change roles
    if update_data.role is not None and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change user roles"
        )

    use_case = UpdateUserUseCase(repository)
    updated_user = use_case.execute(user_id, update_data)

    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        full_name=updated_user.full_name,
        role=updated_user.role,
        is_active=updated_user.is_active,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository)
):
    """
    Delete a user by ID (admin only).

    Returns 204 No Content on success.
    Returns 403 if the caller is not an admin.
    Returns 404 if the user does not exist.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete users"
        )

    use_case = DeleteUserUseCase(repository)
    use_case.execute(user_id)

