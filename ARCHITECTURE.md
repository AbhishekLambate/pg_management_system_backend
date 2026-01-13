# PG Management System - Architecture Document

## 1. System Overview

### 1.1 Purpose
A backend system for managing Paying Guest (PG) accommodations, handling room bookings, tenant management, payments, and administrative operations.

### 1.2 Core Features
- **User Management**: Admin and staff authentication/authorization
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
- **Database**: PostgreSQL (recommended) or SQLite (for development)
- **Migrations**: Alembic

### 2.3 Authentication & Security
- **JWT**: python-jose for token generation/validation
- **Password Hashing**: passlib with bcrypt
- **CORS**: FastAPI CORS middleware

### 2.4 Additional Libraries
- **Environment Variables**: python-dotenv, pydantic-settings
- **Validation**: Pydantic v2
- **Date/Time**: Python datetime (built-in)

---

## 3. Project Structure

```
pg_management_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection & session management
│   │
│   ├── models/                # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── user.py           # User/Admin model
│   │   ├── room.py           # Room model
│   │   ├── tenant.py         # Tenant model
│   │   ├── booking.py        # Booking model
│   │   └── payment.py        # Payment model
│   │
│   ├── schemas/               # Pydantic schemas for request/response validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── tenant.py
│   │   ├── booking.py
│   │   └── payment.py
│   │
│   ├── routers/               # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication routes
│   │   ├── rooms.py           # Room management routes
│   │   ├── tenants.py         # Tenant management routes
│   │   ├── bookings.py        # Booking management routes
│   │   └── payments.py        # Payment management routes
│   │
│   ├── services/              # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Authentication logic
│   │   ├── room_service.py   # Room business logic
│   │   ├── tenant_service.py # Tenant business logic
│   │   ├── booking_service.py # Booking business logic
│   │   └── payment_service.py # Payment business logic
│   │
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py       # Password hashing, JWT tokens
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   └── validators.py     # Custom validators
│   │
│   └── middleware/            # Custom middleware (if needed)
│       └── __init__.py
│
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_rooms.py
│   ├── test_tenants.py
│   └── ...
│
├── .env                        # Environment variables (not in git)
├── .env.example               # Example environment variables
├── .gitignore
├── requirements.txt           # Python dependencies
├── alembic.ini                # Alembic configuration
├── README.md
└── ARCHITECTURE.md            # This file
```

---

## 4. Database Schema Design

### 4.1 Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    User     │         │    Tenant    │         │    Room     │
│─────────────│         │──────────────│         │─────────────│
│ id (PK)     │         │ id (PK)      │         │ id (PK)     │
│ username    │         │ full_name    │         │ room_number │
│ email       │         │ email        │         │ floor       │
│ password    │         │ phone        │         │ room_type   │
│ full_name   │         │ address      │         │ capacity    │
│ is_admin    │         │ id_proof     │         │ rent_amount │
│ is_active   │         │ is_active    │         │ is_available│
└─────────────┘         └──────┬───────┘         └──────┬──────┘
                                │                        │
                                │                        │
                         ┌──────┴────────┐              │
                         │   Booking     │◄─────────────┘
                         │───────────────│
                         │ id (PK)       │
                         │ tenant_id (FK)│
                         │ room_id (FK)  │
                         │ check_in_date │
                         │ check_out_date│
                         │ monthly_rent  │
                         │ status        │
                         └──────┬────────┘
                                │
                                │
                         ┌──────┴────────┐
                         │   Payment     │
                         │───────────────│
                         │ id (PK)       │
                         │ booking_id(FK)│
                         │ amount        │
                         │ payment_date  │
                         │ payment_method│
                         │ status        │
                         └───────────────┘
```

### 4.2 Tables Description

#### 4.2.1 Users Table
- **Purpose**: Store admin/staff user accounts
- **Key Fields**: username, email, hashed_password, is_admin
- **Relationships**: None (standalone)

#### 4.2.2 Rooms Table
- **Purpose**: Store room information and availability
- **Key Fields**: room_number (unique), floor, room_type, capacity, rent_amount
- **Relationships**: One-to-Many with Bookings

#### 4.2.3 Tenants Table
- **Purpose**: Store tenant/potential tenant information
- **Key Fields**: email (unique), phone, full_name, id_proof
- **Relationships**: One-to-Many with Bookings

#### 4.2.4 Bookings Table
- **Purpose**: Track room bookings and occupancy
- **Key Fields**: tenant_id (FK), room_id (FK), check_in_date, status
- **Relationships**: 
  - Many-to-One with Tenant
  - Many-to-One with Room
  - One-to-Many with Payments

#### 4.2.5 Payments Table
- **Purpose**: Track all payment transactions
- **Key Fields**: booking_id (FK), amount, payment_date, payment_method, status
- **Relationships**: Many-to-One with Booking

---

## 5. API Design

### 5.1 API Structure
- **Base URL**: `/api`
- **Versioning**: Not implemented initially (can add `/v1` later)
- **Authentication**: JWT Bearer tokens
- **Response Format**: JSON

### 5.2 Endpoint Groups

#### 5.2.1 Authentication (`/api/auth`)
- `POST /api/auth/register` - Register new admin user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout (token blacklisting)

#### 5.2.2 Rooms (`/api/rooms`)
- `GET /api/rooms` - List all rooms (with filters: available, floor, type)
- `GET /api/rooms/{room_id}` - Get room details
- `POST /api/rooms` - Create new room (admin only)
- `PUT /api/rooms/{room_id}` - Update room (admin only)
- `DELETE /api/rooms/{room_id}` - Delete room (admin only)
- `GET /api/rooms/available` - Get available rooms
- `GET /api/rooms/{room_id}/occupancy` - Get room occupancy history

#### 5.2.3 Tenants (`/api/tenants`)
- `GET /api/tenants` - List all tenants (with pagination, filters)
- `GET /api/tenants/{tenant_id}` - Get tenant details
- `POST /api/tenants` - Create new tenant
- `PUT /api/tenants/{tenant_id}` - Update tenant
- `DELETE /api/tenants/{tenant_id}` - Delete tenant (soft delete)
- `GET /api/tenants/{tenant_id}/bookings` - Get tenant's booking history

#### 5.2.4 Bookings (`/api/bookings`)
- `GET /api/bookings` - List all bookings (with filters: status, date range)
- `GET /api/bookings/{booking_id}` - Get booking details
- `POST /api/bookings` - Create new booking
- `PUT /api/bookings/{booking_id}` - Update booking (check-out, status change)
- `DELETE /api/bookings/{booking_id}` - Cancel booking
- `POST /api/bookings/{booking_id}/checkout` - Check-out tenant
- `GET /api/bookings/active` - Get all active bookings

#### 5.2.5 Payments (`/api/payments`)
- `GET /api/payments` - List all payments (with filters: booking, date range)
- `GET /api/payments/{payment_id}` - Get payment details
- `POST /api/payments` - Record new payment
- `PUT /api/payments/{payment_id}` - Update payment (status, refund)
- `GET /api/payments/booking/{booking_id}` - Get payments for a booking
- `GET /api/payments/reports` - Payment reports (monthly, yearly)

---

## 6. Authentication & Authorization

### 6.1 Authentication Flow
1. User registers/logs in with username and password
2. Server validates credentials
3. Server generates JWT access token (expires in 30 minutes)
4. Client includes token in `Authorization: Bearer <token>` header
5. Server validates token on each protected request

### 6.2 Authorization Levels
- **Admin**: Full access to all endpoints
- **Staff**: Read access to most endpoints, limited write access
- **Public**: Only login/register endpoints

### 6.3 Security Measures
- Password hashing with bcrypt
- JWT tokens with expiration
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)

---

## 7. Data Flow

### 7.1 Request Flow
```
Client Request
    ↓
FastAPI Router (routers/)
    ↓
Authentication Middleware (verify JWT)
    ↓
Authorization Check (verify permissions)
    ↓
Service Layer (services/) - Business Logic
    ↓
Database Layer (models/) - SQLAlchemy ORM
    ↓
Database (PostgreSQL)
    ↓
Response (Pydantic Schema validation)
    ↓
Client Response
```

### 7.2 Example: Creating a Booking
1. Client sends `POST /api/bookings` with booking data
2. Router validates request schema
3. Auth middleware verifies JWT token
4. Booking service:
   - Validates room availability
   - Checks tenant exists
   - Creates booking record
   - Updates room occupancy
5. Returns booking details

---

## 8. Key Business Rules

### 8.1 Room Management
- Room capacity cannot be exceeded
- Room availability updated automatically on booking/checkout
- Cannot delete room with active bookings

### 8.2 Booking Management
- Only one active booking per tenant at a time (optional rule)
- Check-in date must be >= today
- Check-out date must be > check-in date
- Cannot book unavailable rooms

### 8.3 Payment Management
- Payments linked to bookings
- Payment amount validation
- Payment status tracking (pending, completed, failed, refunded)

---

## 9. Error Handling

### 9.1 HTTP Status Codes
- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Pydantic validation errors
- `500 Internal Server Error` - Server errors

### 9.2 Error Response Format
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "field": "field_name" // if validation error
}
```

---

## 10. Development Workflow

### 10.1 Setup Steps
1. Create virtual environment
2. Install dependencies from `requirements.txt`
3. Set up PostgreSQL database
4. Configure `.env` file
5. Run Alembic migrations
6. Start development server

### 10.2 Database Migrations
- Use Alembic for schema changes
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migration: `alembic upgrade head`
- Rollback: `alembic downgrade -1`

### 10.3 Testing Strategy
- Unit tests for services
- Integration tests for API endpoints
- Use pytest framework
- Mock database for unit tests

---

## 11. Future Enhancements

### 11.1 Phase 2 Features
- Email notifications (booking confirmations, payment reminders)
- SMS notifications
- Document upload (ID proofs, contracts)
- Advanced reporting and analytics
- Multi-PG support (if managing multiple properties)
- Mobile app API support

### 11.2 Technical Improvements
- Redis for caching
- Celery for background tasks
- WebSocket for real-time updates
- API rate limiting
- Request logging and monitoring
- Docker containerization
- CI/CD pipeline

---

## 12. Configuration Management

### 12.1 Environment Variables
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `HOST` - Server host
- `PORT` - Server port
- `DEBUG` - Debug mode flag

### 12.2 Configuration Loading
- Use `pydantic-settings` for type-safe configuration
- Load from `.env` file
- Validate on application startup

---

## 13. API Documentation

- **Swagger UI**: Automatically generated at `/docs`
- **ReDoc**: Alternative docs at `/redoc`
- FastAPI auto-generates from code annotations and Pydantic schemas

---

## 14. Deployment Considerations

### 14.1 Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper CORS origins
- [ ] Set up database connection pooling
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Set up monitoring

### 14.2 Recommended Deployment
- **Platform**: AWS, GCP, Azure, or DigitalOcean
- **Server**: Linux (Ubuntu)
- **Process Manager**: systemd or supervisor
- **Reverse Proxy**: Nginx
- **Database**: Managed PostgreSQL service

---

## 15. Questions for Discussion

Before implementation, consider:

1. **Multi-tenancy**: Do we need to support multiple PG properties?
2. **User Roles**: Do we need more granular roles (owner, manager, staff)?
3. **Booking Rules**: Can a tenant have multiple active bookings?
4. **Payment Integration**: Do we need payment gateway integration (Razorpay, Stripe)?
5. **Notifications**: Email/SMS requirements?
6. **Reporting**: What specific reports are needed?
7. **Data Retention**: How long to keep historical data?

---

This architecture document serves as a blueprint for the PG Management System backend. Review and discuss any changes before proceeding with implementation.

