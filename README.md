# PG Management System Backend

Backend API for Paying Guest (PG) Management System built with FastAPI.

## Features Implemented

### ✅ User Management
- User registration and authentication
- JWT-based authentication
- Admin and regular user roles
- User profile management

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

#### Install MySQL (if not already installed)
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install mysql-server

# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure MySQL installation (optional but recommended)
sudo mysql_secure_installation
```

#### Create Database and User
```bash
# Connect to MySQL
sudo mysql -u root -p

# In MySQL prompt, run:
CREATE DATABASE pg_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pg_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON pg_management_db.* TO 'pg_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Using MySQL Workbench (GUI Method - Recommended)
If you prefer using a graphical interface, see **[MYSQL_WORKBENCH_SETUP.md](MYSQL_WORKBENCH_SETUP.md)** for detailed step-by-step instructions on creating the database and user using MySQL Workbench.

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Database Configuration (MySQL)
DATABASE_URL=mysql+pymysql://pg_user:your_password_here@localhost:3306/pg_management_db

# Format: mysql+pymysql://username:password@host:port/database_name
# For local development: mysql+pymysql://pg_user:password@localhost:3306/pg_management_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Note:** Replace `your_password_here` with the actual password you set for the MySQL user.

### 5. Run the Application
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints (Users Feature)

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/register/admin` - Register a new admin (requires admin auth)
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/users` - Get all users (admin only)
- `GET /api/auth/users/{user_id}` - Get specific user (admin or own profile)

## Testing the API

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "Admin User"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### 3. Get Current User (with token)
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure (Clean Architecture)

The project follows Clean Architecture pattern with clear separation of concerns:

```
pg_management_system_backend/
├── app/
│   ├── entities/                    # Domain entities (pure business logic)
│   │   └── user.py                  # User domain entity
│   │
│   ├── repositories/                # Data access layer
│   │   ├── interfaces/              # Repository interfaces (contracts)
│   │   │   └── user_repository_interface.py
│   │   └── user_repository.py      # SQLAlchemy implementation
│   │
│   ├── usecases/                    # Business logic / Use cases
│   │   └── auth_usecase.py          # Authentication use cases
│   │
│   ├── handlers/                    # API route handlers
│   │   └── auth_handler.py          # Authentication endpoints
│   │
│   ├── models/                      # SQLAlchemy ORM models (database layer)
│   │   └── user.py                  # User database model
│   │
│   ├── schemas/                     # Pydantic schemas (request/response)
│   │   └── user.py                  # User schemas
│   │
│   ├── utils/                       # Utilities
│   │   ├── security.py              # Password hashing, JWT
│   │   └── dependencies.py         # FastAPI dependencies
│   │
│   ├── config.py                    # Configuration
│   ├── database.py                  # Database setup
│   └── main.py                      # FastAPI app
│
├── requirements.txt
└── run.py
```

**Note:** The old `routers/` and `services/` directories have been removed as they are replaced by `handlers/` and `usecases/` in the Clean Architecture pattern.

### Architecture Layers:

1. **Entities** (`app/entities/`): Pure domain models with business logic, no dependencies
2. **Repositories** (`app/repositories/`): Data access layer
   - **Interfaces**: Abstract contracts defining repository methods
   - **Implementations**: Concrete implementations (SQLAlchemy, etc.)
3. **Use Cases** (`app/usecases/`): Business logic and application rules
4. **Handlers** (`app/handlers/`): API endpoints that orchestrate use cases
5. **Models** (`app/models/`): SQLAlchemy ORM models for database persistence
6. **Schemas** (`app/schemas/`): Pydantic models for request/response validation

### Data Flow:
```
Request → Handler → Use Case → Repository (Interface) → Repository (Implementation) → Database
         ↓
      Response ← Schema ← Entity ← Repository ← Use Case ← Handler
```

## Next Steps

The users feature is now complete. Next features to implement:
- Room Management
- Tenant Management
- Booking Management
- Payment Management