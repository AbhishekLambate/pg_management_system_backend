# PG Management System - Architecture Document

Complete architecture documentation for the PG Management System backend.

---

## 1. System Overview

### 1.1 Purpose
A backend system for managing Paying Guest (PG) accommodations, handling room bookings, tenant management, payments, and administrative operations.

### 1.2 Core Features
- **User Management**: Role-based authentication/authorization (admin/user)
- **Room Management**: CRUD operations for rooms, availability tracking
- **Tenant Management**: Tenant profiles, contact information, ID verification
- **Booking Management**: Room bookings, check-in/check-out, occupancy tracking
- **Payment Management**: Rent payments, deposits, payment history
- **Reporting**: Occupancy reports, payment reports, revenue tracking

---

## 2. Technology Stack

### 2.1 Framework & Runtime
- **Framework**: FastAPI (modern, fast, async-capable Python web framework)
- **Python Version**: 3.9+
- **ASGI Server**: Uvicorn

### 2.2 Database
- **ORM**: SQLAlchemy 2.0
- **Database**: MySQL (recommended) or SQLite (for development)
- **Driver**: PyMySQL
- **Migrations**: Alembic

### 2.3 Authentication & Security
- **JWT**: python-jose for token generation/validation
- **Password Hashing**: passlib with bcrypt
- **CORS**: FastAPI CORS middleware
- **Email Validation**: email-validator

### 2.4 Additional Libraries
- **Environment Variables**: python-dotenv, pydantic-settings
- **Validation**: Pydantic v2
- **Date/Time**: Python datetime (built-in)

---

## 3. Architecture Pattern: Clean Architecture

The project follows **Clean Architecture** with clear separation of concerns using a restaurant analogy:

- **Handler** = Waiter (takes order, serves food)
- **UseCase** = Chef (cooks the meal, follows recipe)
- **Repository** = Kitchen equipment (tools to get/store ingredients)
- **Interface** = Recipe card (defines what tools are needed)
- **Entity** = Ingredients (data structures)

### 3.1 Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                        Handlers                              │
│              (API Endpoints / HTTP Layer)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                       Use Cases                              │
│              (Business Logic / Application Rules)             │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   Repository Interfaces                      │
│              (Contracts / Abstractions)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  Repository Implementations                  │
│              (Data Access Layer)                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Database                                │
│              (MySQL / SQLAlchemy)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Project Structure

```
pg_management_system_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection & session management
│   │
│   ├── entities/              # Domain entities (pure business logic)
│   │   ├── __init__.py
│   │   └── user.py           # User domain entity
│   │
│   ├── repositories/          # Data access layer
│   │   ├── interfaces/        # Repository interfaces (contracts)
│   │   │   ├── __init__.py
│   │   │   └── user_repository_interface.py
│   │   └── user_repository.py # SQLAlchemy implementation
│   │
│   ├── usecases/              # Business logic / Use cases
│   │   ├── __init__.py
│   │   └── auth_usecase.py   # Authentication use cases
│   │
│   ├── handlers/              # API route handlers
│   │   ├── __init__.py
│   │   └── auth_handler.py   # Authentication endpoints
│   │
│   ├── models/                # SQLAlchemy ORM models (database layer)
│   │   ├── __init__.py
│   │   └── user.py           # User database model
│   │
│   ├── schemas/               # Pydantic schemas (request/response validation)
│   │   ├── __init__.py
│   │   └── user.py           # User schemas
│   │
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py       # Password hashing, JWT tokens
│   │   └── dependencies.py   # FastAPI dependencies
│   │
│   └── middleware/            # Custom middleware (if needed)
│       └── __init__.py
│
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Test files
│   └── __init__.py
│
├── .env                        # Environment variables
├── requirements.txt           # Python dependencies
├── run.py                     # Application runner
└── README.md                  # Project documentation
```

---

## 5. Layer Descriptions

### 5.1 Entities (`app/entities/`)
**Purpose**: Pure domain models with business logic (Ingredients)

**Characteristics**:
- No dependencies on external frameworks
- Contains business rules and validation
- Framework-agnostic

**Example**: `UserEntity` - represents a user in the domain

```python
class UserEntity:
    def __init__(self, username, email, role="user", ...):
        self.role = role  # 'admin' or 'user'
    
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"
```

### 5.2 Repository Interfaces (`app/repositories/interfaces/`)
**Purpose**: Define contracts for data access (Recipe Card)

**Characteristics**:
- Abstract base classes (ABC)
- Define what operations are available
- No implementation details

**Example**: `IUserRepository` - defines methods like `create()`, `get_by_id()`, etc.

### 5.3 Repository Implementations (`app/repositories/`)
**Purpose**: Concrete implementations of repository interfaces (Kitchen Equipment)

**Characteristics**:
- Implements the interface contract
- Handles database-specific logic
- Converts between domain entities and database models

**Example**: `UserRepository` - SQLAlchemy implementation

### 5.4 Use Cases (`app/usecases/`)
**Purpose**: Application-specific business logic (Chef)

**Characteristics**:
- Orchestrates entities and repositories
- Implements application rules
- One use case per business operation

**Examples**:
- `RegisterUserUseCase` - handles user registration
- `LoginUseCase` - handles user authentication
- `GetUserUseCase` - retrieves user information

### 5.5 Handlers (`app/handlers/`)
**Purpose**: HTTP request/response handling (Waiter)

**Characteristics**:
- FastAPI route handlers
- Validates requests using Pydantic schemas
- Calls appropriate use cases
- Converts entities to response schemas

**Example**: `auth_handler.py` - authentication endpoints

### 5.6 Models (`app/models/`)
**Purpose**: SQLAlchemy ORM models for database persistence

**Characteristics**:
- Database-specific
- Used only by repository implementations
- Not exposed to use cases or handlers

### 5.7 Schemas (`app/schemas/`)
**Purpose**: Request/response validation with Pydantic

**Characteristics**:
- Used for API input/output validation
- Separate from domain entities
- Framework-specific (Pydantic)

---

## 6. Database Schema Design

### 6.1 Users Table

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'user',  -- 'admin' or 'user'
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP
);
```

**Key Fields**:
- `role`: 'admin' or 'user' (determines permissions)
- `is_admin`: Computed property (returns `role == "admin"`)

---

## 7. API Design

### 7.1 API Structure
- **Base URL**: `/api`
- **Authentication**: JWT Bearer tokens
- **Response Format**: JSON

### 7.2 Authentication Endpoints (`/api/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user (with role) | No |
| POST | `/api/auth/login` | Login and get JWT token | No |
| GET | `/api/auth/me` | Get current user info | Yes |
| GET | `/api/auth/users` | Get all users | Yes (Admin) |
| GET | `/api/auth/users/{user_id}` | Get specific user | Yes |

### 7.3 Request/Response Examples

#### Register User
**Request:**
```json
POST /api/auth/register
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

#### Login
**Request:**
```json
POST /api/auth/login
{
  "username": "john_doe",
  "password": "john123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 8. Data Flow

### 8.1 Request Flow Example: User Registration

```
1. Client Request
   POST /api/auth/register
   ↓
2. Handler (auth_handler.py)
   - Validates request schema (UserCreate)
   - Gets repository dependency
   ↓
3. UseCase (RegisterUserUseCase)
   - Validates business rules (username/email uniqueness)
   - Creates UserEntity with role
   ↓
4. Repository (UserRepository)
   - Converts UserEntity → User (model)
   - Saves to MySQL database
   - Converts User → UserEntity
   ↓
5. UseCase Returns UserEntity
   ↓
6. Handler Converts to UserResponse (schema)
   ↓
7. Client Receives JSON Response
```

### 8.2 Dependency Direction

```
Handler → UseCase → Interface ← Repository
                ↓
            Entity
```

- Handlers depend on UseCases
- UseCases depend on Interfaces (not implementations!)
- Repositories implement Interfaces
- Entities are independent

---

## 9. Authentication & Authorization

### 9.1 Authentication Flow
1. User registers/logs in with username and password
2. Server validates credentials
3. Server generates JWT access token (expires in 30 minutes)
4. Client includes token in `Authorization: Bearer <token>` header
5. Server validates token on each protected request

### 9.2 Authorization Levels
- **Admin** (role="admin"): Full access to all endpoints
- **User** (role="user"): Limited access, can view own profile

### 9.3 Security Measures
- Password hashing with bcrypt
- JWT tokens with expiration
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)

---

## 10. Key Business Rules

### 10.1 User Management
- Username must be unique
- Email must be unique
- Role must be either "admin" or "user"
- Default role is "user"
- Password minimum length: 6 characters

### 10.2 Role-Based Access
- Only users with `role="admin"` can access admin endpoints
- Regular users can only view their own profile
- `is_admin` is computed from `role` for backward compatibility

---

## 11. Error Handling

### 11.1 HTTP Status Codes
- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Pydantic validation errors
- `500 Internal Server Error` - Server errors

### 11.2 Error Response Format
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "field": "field_name"  // if validation error
}
```

---

## 12. Configuration

### 12.1 Environment Variables (.env)
```env
# Database Configuration (MySQL)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/pg_management_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

---

## 13. Development Workflow

### 13.1 Setup Steps
1. Create virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MySQL database
4. Configure `.env` file
5. Run application: `python run.py`

### 13.2 Database Migrations
- Use Alembic for schema changes
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migration: `alembic upgrade head`

---

## 14. Adding a New Feature

When adding a new feature (e.g., Room Management):

1. **Create Entity**: `app/entities/room.py`
2. **Create Repository Interface**: `app/repositories/interfaces/room_repository_interface.py`
3. **Create Repository Implementation**: `app/repositories/room_repository.py`
4. **Create Use Cases**: `app/usecases/room_usecase.py`
5. **Create Handler**: `app/handlers/room_handler.py`
6. **Create Model**: `app/models/room.py`
7. **Create Schemas**: `app/schemas/room.py`
8. **Register Handler**: Add to `app/main.py`

---

## 15. Benefits of This Architecture

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Clear separation of concerns
3. **Flexibility**: Easy to swap implementations (e.g., change database)
4. **Independence**: Business logic doesn't depend on frameworks
5. **Scalability**: Easy to add new features following the same pattern

---

## 16. API Documentation

- **Swagger UI**: Automatically generated at `/docs`
- **ReDoc**: Alternative docs at `/redoc`
- FastAPI auto-generates from code annotations and Pydantic schemas

---

## 17. Current Implementation Status

### ✅ Implemented
- User Management with role-based access
- JWT Authentication
- Clean Architecture pattern
- MySQL database integration
- API documentation (Swagger)

### 🚧 To Be Implemented
- Room Management
- Tenant Management
- Booking Management
- Payment Management
- Reporting

---

This architecture document reflects the current implementation using Clean Architecture, MySQL database, and role-based user system.
