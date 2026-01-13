# Simple Code Flow - Step by Step

## Example: Register User (`POST /api/auth/register`)

### 📍 Step 1: Request Arrives
```python
# Client sends: POST /api/auth/register
# Body: { "username": "john", "email": "john@example.com", "password": "123", "full_name": "John" }
```

---

### 📍 Step 2: FastAPI Routes to Handler
**File:** `app/main.py`
```python
app.include_router(auth_handler.router)  # ← Routes to auth_handler
```

**File:** `app/handlers/auth_handler.py` - Line 29
```python
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,  # ← FastAPI auto-validates request body
    repository: UserRepository = Depends(get_user_repository)
):
```

**What happens here:**
- ✅ FastAPI validates JSON against `UserCreate` schema
- ✅ If valid → continues, if invalid → returns 422 error

---

### 📍 Step 3: Handler Gets Repository
**File:** `app/handlers/auth_handler.py` - Line 18
```python
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)  # ← Creates repository with database session
```

**What happens here:**
- ✅ FastAPI dependency injection creates database session
- ✅ Creates `UserRepository` instance
- ✅ Passes to `register()` function

---

### 📍 Step 4: Handler Creates UseCase
**File:** `app/handlers/auth_handler.py` - Line 42
```python
use_case = RegisterUserUseCase(repository)  # ← Chef gets equipment
```

**What happens here:**
- ✅ Handler creates UseCase instance
- ✅ Passes repository (equipment) to UseCase (chef)

---

### 📍 Step 5: UseCase Executes Business Logic
**File:** `app/handlers/auth_handler.py` - Line 44
```python
user_entity = use_case.execute(user_data, is_admin=False)  # ← Chef cooks
```

**File:** `app/usecases/auth_usecase.py` - Line 17
```python
def execute(self, user_data: UserCreate, is_admin: bool = False) -> UserEntity:
    # Step 5a: Check username exists
    existing_user = self.user_repository.get_by_username(user_data.username)
    # ↑ Calls repository method (following interface recipe)
    
    if existing_user:
        raise HTTPException(...)  # ← Business rule: username must be unique
    
    # Step 5b: Check email exists
    existing_email = self.user_repository.get_by_email(user_data.email)
    # ↑ Calls repository method again
    
    if existing_email:
        raise HTTPException(...)  # ← Business rule: email must be unique
    
    # Step 5c: Create entity (ingredients)
    hashed_password = get_password_hash(user_data.password)
    user_entity = UserEntity(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_admin=is_admin,
        is_active=True
    )
    
    # Step 5d: Save using repository
    return self.user_repository.create(user_entity)  # ← Store ingredients
```

**What happens here:**
- ✅ UseCase validates business rules (uniqueness)
- ✅ Creates `UserEntity` (domain model)
- ✅ Calls `repository.create()` to save

---

### 📍 Step 6: Repository Saves to Database
**File:** `app/repositories/user_repository.py` - Line 40
```python
def create(self, user: UserEntity) -> UserEntity:
    # Step 6a: Convert Entity → Model (for database)
    db_user = self._to_model(user)  # UserEntity → User (SQLAlchemy)
    
    # Step 6b: Save to database
    self.db.add(db_user)
    self.db.commit()
    self.db.refresh(db_user)
    
    # Step 6c: Convert Model → Entity (back to domain)
    return self._to_entity(db_user)  # User → UserEntity
```

**File:** `app/models/user.py` - The database model
```python
class User(Base):  # ← SQLAlchemy ORM model
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    # ... stored in MySQL
```

**What happens here:**
- ✅ Converts `UserEntity` → `User` (database format)
- ✅ Saves to MySQL database
- ✅ Converts back `User` → `UserEntity`
- ✅ Returns `UserEntity` to UseCase

---

### 📍 Step 7: UseCase Returns to Handler
**File:** `app/usecases/auth_usecase.py` - Line 47
```python
return self.user_repository.create(user_entity)  # ← Returns UserEntity
```

**File:** `app/handlers/auth_handler.py` - Line 44
```python
user_entity = use_case.execute(...)  # ← Receives UserEntity
```

---

### 📍 Step 8: Handler Converts to Response
**File:** `app/handlers/auth_handler.py` - Line 47
```python
return UserResponse(  # ← Convert Entity → Response Schema
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

**What happens here:**
- ✅ Handler converts `UserEntity` → `UserResponse` (Pydantic schema)
- ✅ FastAPI auto-serializes to JSON
- ✅ Returns HTTP 201 Created

---

### 📍 Step 9: Response Sent to Client
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "full_name": "John",
  "is_admin": false,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null
}
```

---

## Quick Reference: File Order

```
1. app/main.py                    → Routes request
2. app/handlers/auth_handler.py   → Handler receives request
3. app/usecases/auth_usecase.py   → UseCase executes logic
4. app/repositories/user_repository.py → Repository saves data
5. app/models/user.py             → Database model (SQLAlchemy)
6. app/repositories/user_repository.py → Converts back to Entity
7. app/usecases/auth_usecase.py   → Returns Entity
8. app/handlers/auth_handler.py   → Converts to Response
9. Client receives JSON response
```

---

## Data Transformations

```
Request JSON
    ↓
UserCreate (Schema) ← Validation
    ↓
UserEntity (Domain) ← Business Logic
    ↓
User (Model) ← Database Storage
    ↓
[Database] ← MySQL
    ↓
User (Model) ← Retrieved
    ↓
UserEntity (Domain) ← Back to Domain
    ↓
UserResponse (Schema) ← API Response
    ↓
Response JSON
```

---

## Key Files & Their Roles

| File | Role | What It Does |
|------|------|--------------|
| `handlers/auth_handler.py` | Waiter | Takes order, serves food |
| `usecases/auth_usecase.py` | Chef | Cooks meal, follows recipe |
| `repositories/user_repository.py` | Equipment | Stores/retrieves ingredients |
| `repositories/interfaces/user_repository_interface.py` | Recipe | Defines what equipment can do |
| `entities/user.py` | Ingredients | Pure data structures |
| `models/user.py` | Storage | Database format |
| `schemas/user.py` | Order/Response Format | API validation |

