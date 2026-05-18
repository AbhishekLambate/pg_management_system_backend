# Code Flow Documentation

This document shows exactly how code flows through the system using a real example.

## Example: User Registration Flow

Let's trace a complete request: `POST /api/auth/register`

---

## Step-by-Step Flow

### Step 1: Client Makes Request
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123",
  "full_name": "John Doe"
}
```

---

### Step 2: FastAPI Routes to Handler
**File:** `app/main.py`
```python
app.include_router(auth_handler.router)  # Routes to auth_handler
```

**File:** `app/handlers/auth_handler.py`
```python
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,  # ← FastAPI validates request against UserCreate schema
    repository: UserRepository = Depends(get_user_repository)
):
```

**What happens:**
- FastAPI receives HTTP request
- Validates request body against `UserCreate` schema (from `app/schemas/user.py`)
- If valid, calls `register()` function
- If invalid, returns 422 error

---

### Step 3: Handler Gets Repository (Kitchen Equipment)
**File:** `app/handlers/auth_handler.py`
```python
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Provides kitchen equipment (Repository implementation)"""
    return UserRepository(db)  # ← Creates actual repository with database session
```

**What happens:**
- FastAPI dependency injection creates database session
- Creates `UserRepository` instance with database session
- Passes it to the handler function

---

### Step 4: Handler Creates UseCase (Gives Equipment to Chef)
**File:** `app/handlers/auth_handler.py`
```python
def register(...):
    # Waiter gives the kitchen equipment to the Chef
    use_case = RegisterUserUseCase(repository)  # ← Chef gets the equipment
    # Chef prepares the meal (executes business logic)
    user_entity = use_case.execute(user_data, is_admin=False)  # ← Chef cooks
```

**What happens:**
- Handler creates `RegisterUserUseCase` instance
- Passes `UserRepository` (equipment) to the UseCase (Chef)
- Calls `execute()` method with user data

---

### Step 5: UseCase Follows Recipe (Interface)
**File:** `app/usecases/auth_usecase.py`
```python
class RegisterUserUseCase:
    def __init__(self, user_repository: IUserRepository):  # ← Uses Interface (Recipe)
        self.user_repository = user_repository  # ← Chef gets equipment
    
    def execute(self, user_data: UserCreate, is_admin: bool = False) -> UserEntity:
        # Check if username already exists
        existing_user = self.user_repository.get_by_username(user_data.username)
        # ↑ Chef uses equipment following recipe (interface methods)
        
        if existing_user:
            raise HTTPException(...)  # ← Business rule validation
        
        # Check if email already exists
        existing_email = self.user_repository.get_by_email(user_data.email)
        # ↑ Chef uses equipment again
        
        # Create user entity (ingredients)
        hashed_password = get_password_hash(user_data.password)
        user_entity = UserEntity(  # ← Creating ingredients
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_admin=is_admin,
            is_active=True
        )
        
        # Save to repository (store ingredients)
        return self.user_repository.create(user_entity)  # ← Chef uses equipment to store
```

**What happens:**
1. UseCase checks if username exists (calls `repository.get_by_username()`)
2. UseCase checks if email exists (calls `repository.get_by_email()`)
3. UseCase creates `UserEntity` (ingredients) with hashed password
4. UseCase calls `repository.create()` to save the entity

**Key Point:** UseCase only knows about `IUserRepository` interface (recipe), not the implementation!

---

### Step 6: Repository Implementation (Equipment Works)
**File:** `app/repositories/user_repository.py`
```python
class UserRepository(IUserRepository):  # ← Implements the recipe (interface)
    def __init__(self, db: Session):
        self.db = db  # ← Equipment has database connection
    
    def create(self, user: UserEntity) -> UserEntity:
        """Equipment knows HOW to store ingredients"""
        # Convert ingredient (Entity) to storage format (Model)
        db_user = self._to_model(user)  # ← UserEntity → User (SQLAlchemy model)
        
        # Store in database
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # Convert back to ingredient format
        return self._to_entity(db_user)  # ← User → UserEntity
```

**What happens:**
1. Repository receives `UserEntity` (ingredient)
2. Converts to `User` model (storage format) using `_to_model()`
3. Saves to database using SQLAlchemy
4. Converts back to `UserEntity` using `_to_entity()`
5. Returns `UserEntity` to UseCase

**File:** `app/models/user.py` (Database Model)
```python
class User(Base):  # ← SQLAlchemy ORM model
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    # ... etc
```

---

### Step 7: UseCase Returns Entity to Handler
**File:** `app/usecases/auth_usecase.py`
```python
return self.user_repository.create(user_entity)  # ← Returns UserEntity
```

**File:** `app/handlers/auth_handler.py`
```python
user_entity = use_case.execute(user_data, is_admin=False)  # ← Receives UserEntity
```

---

### Step 8: Handler Converts Entity to Response Schema
**File:** `app/handlers/auth_handler.py`
```python
def register(...):
    user_entity = use_case.execute(user_data, is_admin=False)
    
    # Convert entity to response (Waiter serves food)
    return UserResponse(  # ← Pydantic schema for response
        id=user_entity.id,
        username=user_entity.username,
        email=user_entity.email,
        full_name=user_entity.full_name,
        is_admin=user_entity.is_admin,
        is_active=user_entity.is_active,
        created_at=user_entity.created_at,
        updated_at=user_entity.updated_at
    )
```

**What happens:**
- Handler converts `UserEntity` to `UserResponse` schema
- FastAPI automatically serializes to JSON
- Returns HTTP 201 Created with response body

---

### Step 9: Response Sent to Client
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_admin": false,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null
}
```

---

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CLIENT REQUEST                                               │
│ POST /api/auth/register                                         │
│ { username, email, password, full_name }                       │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. HANDLER (Waiter) - app/handlers/auth_handler.py              │
│ • Receives request                                               │
│ • Validates against UserCreate schema                            │
│ • Gets UserRepository (equipment)                               │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. USECASE (Chef) - app/usecases/auth_usecase.py               │
│ • Receives UserRepository (equipment)                           │
│ • Follows IUserRepository interface (recipe)                    │
│ • Validates business rules (username/email uniqueness)           │
│ • Creates UserEntity (ingredients)                              │
│ • Calls repository.create()                                     │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. REPOSITORY (Equipment) - app/repositories/user_repository.py│
│ • Implements IUserRepository interface                          │
│ • Converts UserEntity → User (model)                            │
│ • Saves to database (app/models/user.py)                        │
│ • Converts User → UserEntity                                    │
│ • Returns UserEntity                                            │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. USECASE Returns UserEntity to Handler                       │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. HANDLER Converts to Response                                 │
│ • UserEntity → UserResponse (schema)                            │
│ • Returns HTTP 201 with JSON                                    │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. CLIENT RECEIVES RESPONSE                                     │
│ { id, username, email, ... }                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Another Example: Login Flow

### Request
```http
POST /api/auth/login
{
  "username": "john_doe",
  "password": "secure123"
}
```

### Flow

1. **Handler** (`auth_handler.py`) receives `UserLogin` schema
2. **Handler** creates `LoginUseCase` with `UserRepository`
3. **UseCase** (`auth_usecase.py`):
   - Calls `repository.get_by_username()` (following interface)
   - Verifies password using `verify_password()`
   - Checks if user is active
   - Creates JWT token
   - Returns token + user
4. **Repository** (`user_repository.py`):
   - Queries database for user
   - Returns `UserEntity`
5. **Handler** converts to `Token` response schema
6. **Client** receives JWT token

---

## Key Points

1. **Handler** = Entry point, validates input, orchestrates flow
2. **UseCase** = Business logic, depends on Interface (not implementation)
3. **Repository** = Data access, implements Interface
4. **Entity** = Pure domain model, no dependencies
5. **Interface** = Contract that UseCase depends on

## Dependency Direction

```
Handler → UseCase → Interface ← Repository
                ↓
            Entity
```

- Handlers depend on UseCases
- UseCases depend on Interfaces (not implementations!)
- Repositories implement Interfaces
- Entities are independent

This allows:
- Testing UseCases with mock repositories
- Swapping repository implementations
- Keeping business logic independent of database

