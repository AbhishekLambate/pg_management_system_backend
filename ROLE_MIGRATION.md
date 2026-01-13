# Role-Based User System - Migration Guide

The system has been updated to use a **role-based** approach instead of separate admin/user registration endpoints.

---

## What Changed

### Before:
- Two separate endpoints: `/api/auth/register` and `/api/auth/register/admin`
- `is_admin` boolean field in database
- Admin registration required existing admin authentication

### After:
- **Single endpoint**: `/api/auth/register`
- `role` field in database (values: `"admin"` or `"user"`)
- Role specified in registration request JSON
- `is_admin` is now a computed property based on `role`

---

## Database Changes

### New Column:
- **`role`** (VARCHAR(20)): Stores `"admin"` or `"user"`, default is `"user"`

### Migration Needed:
If you have existing data, you'll need to migrate:

```sql
-- Add role column
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';

-- Update existing admin users
UPDATE users SET role = 'admin' WHERE is_admin = true;

-- Update existing regular users
UPDATE users SET role = 'user' WHERE is_admin = false;

-- Make role NOT NULL after setting defaults
ALTER TABLE users MODIFY COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';
```

---

## API Changes

### Single Registration Endpoint

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "john123",
  "full_name": "John Doe",
  "role": "user"  // or "admin"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2026-01-13T12:00:00",
  "updated_at": null
}
```

### Role Validation:
- `role` must be either `"admin"` or `"user"`
- Default value is `"user"` if not provided
- Invalid role values will return validation error

---

## Removed Endpoint

**Removed:** `POST /api/auth/register/admin`

This endpoint no longer exists. Use the single `/api/auth/register` endpoint with `role: "admin"` instead.

---

## Examples

### Register Regular User:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "email": "user1@example.com",
    "password": "password123",
    "full_name": "Regular User",
    "role": "user"
  }'
```

### Register Admin User:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "email": "admin1@example.com",
    "password": "admin123",
    "full_name": "Admin User",
    "role": "admin"
  }'
```

### Register User (role defaults to "user"):
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user2",
    "email": "user2@example.com",
    "password": "password123",
    "full_name": "Another User"
  }'
# role will default to "user" if not provided
```

---

## Code Structure

### Model (`app/models/user.py`):
```python
class User(Base):
    role = Column(String(20), default="user", nullable=False)
    
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"
```

### Entity (`app/entities/user.py`):
```python
class UserEntity:
    role: str = "user"
    
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"
```

### Schema (`app/schemas/user.py`):
```python
class UserCreate(UserBase):
    role: str = Field(default="user")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ["admin", "user"]:
            raise ValueError("Role must be either 'admin' or 'user'")
        return v
```

---

## Backward Compatibility

The `is_admin` property still works for backward compatibility:
- `user.is_admin` returns `True` if `role == "admin"`
- All existing code checking `is_admin` will continue to work
- Response includes `role` field instead of `is_admin` boolean

---

## Testing

### Test 1: Register with role "user"
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test123", "role": "user"}'
```

### Test 2: Register with role "admin"
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testadmin", "email": "admin@example.com", "password": "admin123", "role": "admin"}'
```

### Test 3: Register without role (defaults to "user")
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "defaultuser", "email": "default@example.com", "password": "pass123"}'
```

### Test 4: Invalid role (should fail)
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "invalid", "email": "invalid@example.com", "password": "pass123", "role": "invalid"}'
# Should return 422 validation error
```

---

## Benefits

1. **Simpler API**: One endpoint instead of two
2. **More Flexible**: Easy to add more roles in the future (e.g., "manager", "staff")
3. **Clearer Intent**: Role is explicit in the request
4. **Better Design**: Role-based access control (RBAC) pattern

---

That's it! The system now uses a single registration endpoint with role-based access control! 🎉

