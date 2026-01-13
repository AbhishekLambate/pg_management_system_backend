# Testing Authentication APIs - Step by Step Guide

This guide shows you exactly how to test all authentication endpoints.

---

## Prerequisites

1. **Server must be running**
   ```bash
   python run.py
   ```

2. **Server URL**: `http://localhost:8000`

---

## Method 1: Using Swagger UI (Easiest - Recommended)

### Step 1: Open Swagger UI
Open your browser and go to:
```
http://localhost:8000/docs
```

### Step 2: Test Each Endpoint

#### Test 1: Register a User

1. Find **`POST /api/auth/register`** in the list
2. Click on it to expand
3. Click **"Try it out"** button
4. Fill in the request body:
   ```json
   {
     "username": "john_doe",
     "email": "john@example.com",
     "password": "john123",
     "full_name": "John Doe"
   }
   ```
5. Click **"Execute"**
6. See the response below (should be 201 Created)

#### Test 2: Login

1. Find **`POST /api/auth/login`**
2. Click **"Try it out"**
3. Fill in:
   ```json
   {
     "username": "john_doe",
     "password": "john123"
   }
   ```
4. Click **"Execute"**
5. **Copy the `access_token`** from the response - you'll need it!

#### Test 3: Get Current User (Authenticated)

1. Find **`GET /api/auth/me`**
2. Click **"Try it out"**
3. Click **"Authorize"** button at the top right
4. In the popup, enter: `Bearer YOUR_ACCESS_TOKEN`
   - Replace `YOUR_ACCESS_TOKEN` with the token from login
5. Click **"Authorize"** then **"Close"**
6. Click **"Execute"** on the endpoint
7. You should see your user information

#### Test 4: Get All Users (Admin Only)

1. Find **`GET /api/auth/users`**
2. Click **"Try it out"**
3. Make sure you're authorized (use the token)
4. Click **"Execute"**
5. You'll get 403 Forbidden if you're not admin, or list of users if you are

---

## Method 2: Using curl (Command Line)

### Step 1: Register a User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "jane123",
    "full_name": "Jane Doe"
  }'
```

**Expected Response:**
```json
{
  "id": 2,
  "username": "jane_doe",
  "email": "jane@example.com",
  "full_name": "Jane Doe",
  "is_admin": false,
  "is_active": true,
  "created_at": "2026-01-13T12:00:00",
  "updated_at": null
}
```

### Step 2: Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "password": "jane123"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYW5lX2RvZSIsImV4cCI6MTYxMDQ1NjAwMH0...",
  "token_type": "bearer"
}
```

**Save the token!** Copy the `access_token` value.

### Step 3: Get Current User

Replace `YOUR_TOKEN_HERE` with the actual token:

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response:**
```json
{
  "id": 2,
  "username": "jane_doe",
  "email": "jane@example.com",
  "full_name": "Jane Doe",
  "is_admin": false,
  "is_active": true,
  "created_at": "2026-01-13T12:00:00",
  "updated_at": null
}
```

### Step 4: Get All Users (Admin Only)

```bash
curl -X GET "http://localhost:8000/api/auth/users" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**If not admin, you'll get:**
```json
{
  "detail": "Only admins can view all users"
}
```

### Step 5: Get Specific User

```bash
curl -X GET "http://localhost:8000/api/auth/users/2" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Method 3: Complete Test Script

Save this as `test_auth.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Testing Authentication APIs"
echo "=========================================="
echo ""

# Test 1: Register
echo "1. Testing User Registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }')

echo "$REGISTER_RESPONSE" | python3 -m json.tool
echo ""

# Test 2: Login
echo "2. Testing Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }')

echo "$LOGIN_RESPONSE" | python3 -m json.tool

# Extract token
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo ""
echo "Token extracted: ${TOKEN:0:50}..."
echo ""

# Test 3: Get Current User
echo "3. Testing Get Current User (Authenticated)..."
ME_RESPONSE=$(curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN")
echo "$ME_RESPONSE" | python3 -m json.tool
echo ""

# Test 4: Get All Users
echo "4. Testing Get All Users..."
USERS_RESPONSE=$(curl -s -X GET "$BASE_URL/api/auth/users" \
  -H "Authorization: Bearer $TOKEN")
echo "$USERS_RESPONSE" | python3 -m json.tool
echo ""

echo "=========================================="
echo "✅ All tests completed!"
echo "=========================================="
```

Make it executable and run:
```bash
chmod +x test_auth.sh
./test_auth.sh
```

---

## Method 4: Using Python (requests library)

Create `test_auth.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 50)
print("Testing Authentication APIs")
print("=" * 50)
print()

# Test 1: Register
print("1. Registering user...")
register_data = {
    "username": "python_user",
    "email": "python@example.com",
    "password": "python123",
    "full_name": "Python User"
}
response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

# Test 2: Login
print("2. Logging in...")
login_data = {
    "username": "python_user",
    "password": "python123"
}
response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")
token = response.json()["access_token"]
print(f"Token: {token[:50]}...")
print()

# Test 3: Get Current User
print("3. Getting current user...")
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

# Test 4: Get All Users
print("4. Getting all users...")
response = requests.get(f"{BASE_URL}/api/auth/users", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

print("=" * 50)
print("✅ All tests completed!")
print("=" * 50)
```

Run it:
```bash
pip install requests
python test_auth.py
```

---

## Testing Error Cases

### Test 1: Register with Duplicate Username

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "different@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

**Expected:** `400 Bad Request` - "Username already registered"

### Test 2: Register with Duplicate Email

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "differentuser",
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User"
  }'
```

**Expected:** `400 Bad Request` - "Email already registered"

### Test 3: Login with Wrong Password

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "wrongpassword"
  }'
```

**Expected:** `401 Unauthorized` - "Incorrect username or password"

### Test 4: Access Protected Endpoint Without Token

```bash
curl -X GET "http://localhost:8000/api/auth/me"
```

**Expected:** `401 Unauthorized` - "Not authenticated"

### Test 5: Access with Invalid Token

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer invalid_token_here"
```

**Expected:** `401 Unauthorized` - "Could not validate credentials"

---

## Quick Reference: All Auth Endpoints

| Endpoint | Method | Body | Headers | Response |
|----------|--------|------|---------|----------|
| `/api/auth/register` | POST | username, email, password, full_name | - | User object (201) |
| `/api/auth/login` | POST | username, password | - | Token (200) |
| `/api/auth/me` | GET | - | Authorization: Bearer TOKEN | User object (200) |
| `/api/auth/users` | GET | - | Authorization: Bearer TOKEN | List of users (200) |
| `/api/auth/users/{id}` | GET | - | Authorization: Bearer TOKEN | User object (200) |
| `/api/auth/register/admin` | POST | username, email, password, full_name | Authorization: Bearer TOKEN | User object (201) |

---

## Step-by-Step Testing Workflow

### Complete Flow:

1. **Start Server**
   ```bash
   python run.py
   ```

2. **Register First User**
   - Use Swagger UI or curl
   - Note the user ID

3. **Login**
   - Get the access token
   - Save it somewhere

4. **Test Authenticated Endpoints**
   - Use token in Authorization header
   - Test `/api/auth/me`
   - Test `/api/auth/users`

5. **Test Error Cases**
   - Try duplicate registration
   - Try wrong password
   - Try without token

6. **Create Admin User** (if needed)
   - First, manually set a user as admin in database, OR
   - Use `/api/auth/register/admin` with admin token

---

## Using Postman

1. **Create Collection**: "PG Management Auth"

2. **Add Requests**:

   **Register User:**
   - Method: POST
   - URL: `http://localhost:8000/api/auth/register`
   - Body (raw JSON):
     ```json
     {
       "username": "postman_user",
       "email": "postman@example.com",
       "password": "postman123",
       "full_name": "Postman User"
     }
     ```

   **Login:**
   - Method: POST
   - URL: `http://localhost:8000/api/auth/login`
   - Body (raw JSON):
     ```json
     {
       "username": "postman_user",
       "password": "postman123"
     }
     ```
   - **Tests Tab**: Add this to save token
     ```javascript
     var jsonData = pm.response.json();
     pm.environment.set("auth_token", jsonData.access_token);
     ```

   **Get Current User:**
   - Method: GET
   - URL: `http://localhost:8000/api/auth/me`
   - Authorization: Bearer Token
   - Token: `{{auth_token}}` (from environment variable)

---

## Expected Status Codes

- **200 OK** - Successful GET requests
- **201 Created** - Successful registration
- **400 Bad Request** - Validation errors (duplicate username/email)
- **401 Unauthorized** - Missing/invalid token, wrong credentials
- **403 Forbidden** - Insufficient permissions (not admin)
- **404 Not Found** - User not found
- **422 Unprocessable Entity** - Invalid request body format

---

## Tips

1. **Use Swagger UI** for the easiest testing experience
2. **Save tokens** when testing authenticated endpoints
3. **Test error cases** to ensure proper error handling
4. **Check database** in MySQL Workbench to verify data is saved
5. **Use environment variables** in Postman to manage tokens easily

---

That's it! You now know how to test all authentication APIs! 🎉

