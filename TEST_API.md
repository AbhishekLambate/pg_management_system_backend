# API Testing Guide

This guide shows you how to test the PG Management System API.

---

## Step 1: Start the Server

Run the application:

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 2: Access API Documentation

Once the server is running, open your browser and go to:

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Alternative)**: http://localhost:8000/redoc

The Swagger UI allows you to test all endpoints directly from the browser!

---

## Step 3: Test Endpoints

### Method 1: Using Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. You'll see all available endpoints
3. Click on an endpoint (e.g., `POST /api/auth/register`)
4. Click "Try it out"
5. Fill in the request body
6. Click "Execute"
7. See the response below

### Method 2: Using curl (Command Line)

#### Test 1: Register a New User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_admin": false,
  "is_active": true,
  "created_at": "2024-01-13T16:00:00",
  "updated_at": null
}
```

#### Test 2: Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save the token** for authenticated requests!

#### Test 3: Get Current User (Requires Authentication)

Replace `YOUR_TOKEN_HERE` with the token from login:

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_admin": false,
  "is_active": true,
  "created_at": "2024-01-13T16:00:00",
  "updated_at": null
}
```

#### Test 4: Get All Users (Admin Only)

```bash
curl -X GET "http://localhost:8000/api/auth/users" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Test 5: Get Specific User

```bash
curl -X GET "http://localhost:8000/api/auth/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Step 4: Test with Python (requests library)

Create a test file `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Test 1: Register User
print("1. Registering user...")
response = requests.post(
    f"{BASE_URL}/api/auth/register",
    json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    }
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 2: Login
print("2. Logging in...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "username": "testuser",
        "password": "test123"
    }
)
token = response.json()["access_token"]
print(f"Status: {response.status_code}")
print(f"Token: {token[:50]}...\n")

# Test 3: Get Current User
print("3. Getting current user...")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")
```

Run it:
```bash
pip install requests
python test_api.py
```

---

## Available Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/register/admin` | Register admin user | Yes (Admin) |
| POST | `/api/auth/login` | Login and get token | No |
| GET | `/api/auth/me` | Get current user info | Yes |
| GET | `/api/auth/users` | Get all users | Yes (Admin) |
| GET | `/api/auth/users/{user_id}` | Get specific user | Yes |

---

## Testing Workflow

### Complete Test Flow:

1. **Start Server**
   ```bash
   python run.py
   ```

2. **Register a User**
   - Use Swagger UI or curl
   - Note the user ID returned

3. **Login**
   - Get the access token
   - Save it for authenticated requests

4. **Test Authenticated Endpoints**
   - Use the token in Authorization header
   - Test `/api/auth/me`
   - Test `/api/auth/users` (if admin)

5. **Test Error Cases**
   - Try registering with duplicate username
   - Try logging in with wrong password
   - Try accessing protected endpoint without token

---

## Common Test Scenarios

### Scenario 1: Register and Login Flow

```bash
# 1. Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "john123", "full_name": "John Doe"}'

# 2. Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "john123"}'

# 3. Use token to get profile
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Scenario 2: Create Admin User

First, register a regular user and login to get a token, then:

```bash
curl -X POST "http://localhost:8000/api/auth/register/admin" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"username": "admin", "email": "admin@example.com", "password": "admin123", "full_name": "Admin User"}'
```

**Note:** This requires an existing admin user. For the first admin, you may need to manually update the database or create it directly.

---

## Expected Status Codes

- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST (registration)
- `400 Bad Request` - Validation errors
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Pydantic validation errors

---

## Troubleshooting

### Issue: "Connection refused"
- **Solution**: Make sure the server is running (`python run.py`)

### Issue: "401 Unauthorized"
- **Solution**: Check if you're including the token in the Authorization header
- Format: `Authorization: Bearer YOUR_TOKEN`

### Issue: "422 Unprocessable Entity"
- **Solution**: Check request body format and required fields
- Make sure Content-Type is `application/json`

### Issue: "Database connection error"
- **Solution**: 
  - Check MySQL is running: `sudo systemctl status mysql`
  - Verify `.env` file has correct DATABASE_URL
  - Check database exists in MySQL

---

## Quick Test Script

Save this as `quick_test.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing API..."

# Register
echo "1. Registering user..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test123", "full_name": "Test User"}')
echo "$REGISTER_RESPONSE" | python -m json.tool

# Login
echo -e "\n2. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test123"}')
TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Token: ${TOKEN:0:50}..."

# Get current user
echo -e "\n3. Getting current user..."
curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool

echo -e "\n✅ Tests completed!"
```

Make it executable and run:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

---

## Using Postman or Insomnia

1. **Import Collection**: Create a new collection
2. **Set Base URL**: `http://localhost:8000`
3. **Add Requests**:
   - POST `/api/auth/register`
   - POST `/api/auth/login`
   - GET `/api/auth/me` (with Bearer token)
4. **Set Authorization**: 
   - Type: Bearer Token
   - Token: (from login response)

---

That's it! You're ready to test your API! 🎉

