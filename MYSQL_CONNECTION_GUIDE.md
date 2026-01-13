# MySQL Connection Guide - Backend Code

This guide explains how the MySQL connection works in the backend code.

---

## How MySQL Connection Works

The MySQL connection is handled automatically through SQLAlchemy. Here's how it works:

### 1. Connection String Format

The connection string tells SQLAlchemy how to connect to MySQL:

```
mysql+pymysql://username:password@host:port/database_name
```

**Components:**
- `mysql+pymysql://` - Protocol and driver (pymysql is the Python MySQL driver)
- `username` - MySQL username (e.g., `pg_user`)
- `password` - MySQL password
- `host` - MySQL server address (usually `localhost` or `127.0.0.1`)
- `port` - MySQL port (default is `3306`)
- `database_name` - Database name (e.g., `pg_management_db`)

---

## Step-by-Step Connection Flow

### Step 1: Configuration (`app/config.py`)

```python
class Settings(BaseSettings):
    # Database connection string
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/pg_management_db"
    
    class Config:
        env_file = ".env"  # Loads from .env file
```

**What happens:**
- Reads `DATABASE_URL` from `.env` file
- Falls back to default if `.env` doesn't exist
- Validates the connection string format

---

### Step 2: Database Engine (`app/database.py`)

```python
from sqlalchemy import create_engine
from app.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,  # Connection string from config
    pool_size=10,           # Number of connections to keep in pool
    max_overflow=20,        # Maximum overflow connections
    pool_pre_ping=True,      # Verify connections before using
    echo=settings.DEBUG     # Log SQL queries in debug mode
)
```

**What happens:**
- SQLAlchemy creates a connection pool
- Connection pool manages multiple database connections
- `pool_pre_ping=True` checks if connection is alive before using
- `echo=True` logs all SQL queries (useful for debugging)

---

### Step 3: Session Factory (`app/database.py`)

```python
from sqlalchemy.orm import sessionmaker

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit transactions
    autoflush=False,   # Don't auto-flush changes
    bind=engine       # Use the engine we created
)
```

**What happens:**
- Creates a factory for database sessions
- Each session represents a database connection
- Sessions are used to execute queries

---

### Step 4: Dependency Injection (`app/database.py`)

```python
def get_db():
    """Dependency to get database session."""
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Provide session to the request
    finally:
        db.close()  # Close session after request
```

**What happens:**
- FastAPI calls this function for each request
- Creates a new database session
- Provides session to route handlers
- Automatically closes session after request completes

---

### Step 5: Using in Handlers (`app/handlers/auth_handler.py`)

```python
from app.database import get_db
from sqlalchemy.orm import Session

@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)  # ← FastAPI injects database session
):
    # Use db session to interact with database
    repository = UserRepository(db)
    # ... rest of the code
```

**What happens:**
- FastAPI automatically calls `get_db()` when handler is invoked
- Provides `db` session to the handler
- Handler uses session through repository
- Session is closed automatically after handler completes

---

## Configuration Setup

### Option 1: Using .env File (Recommended)

Create a `.env` file in the project root:

```env
# MySQL Database Configuration
DATABASE_URL=mysql+pymysql://pg_user:your_password@localhost:3306/pg_management_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Important:** Replace `your_password` with your actual MySQL password!

### Option 2: Environment Variables

Set environment variables directly:

```bash
export DATABASE_URL="mysql+pymysql://pg_user:password@localhost:3306/pg_management_db"
export SECRET_KEY="your-secret-key"
```

### Option 3: Direct in Code (Not Recommended)

You can hardcode in `app/config.py`, but this is **NOT recommended** for production:

```python
DATABASE_URL: str = "mysql+pymysql://pg_user:password@localhost:3306/pg_management_db"
```

---

## Connection String Examples

### Local Development
```python
DATABASE_URL = "mysql+pymysql://pg_user:password@localhost:3306/pg_management_db"
```

### Remote MySQL Server
```python
DATABASE_URL = "mysql+pymysql://pg_user:password@192.168.1.100:3306/pg_management_db"
```

### With SSL (Production)
```python
DATABASE_URL = "mysql+pymysql://pg_user:password@host:3306/pg_management_db?ssl_ca=/path/to/ca.pem"
```

### With Special Characters in Password
If your password contains special characters, URL encode them:
```python
# Password: my@pass#word
# Encoded: my%40pass%23word
DATABASE_URL = "mysql+pymysql://pg_user:my%40pass%23word@localhost:3306/pg_management_db"
```

---

## Testing the Connection

### Method 1: Run the Application

```bash
python run.py
```

If connection is successful:
- Application starts without errors
- Tables are created automatically (if using `Base.metadata.create_all()`)
- You can access API at `http://localhost:8000`

If connection fails, you'll see an error like:
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")
```

### Method 2: Test Connection Script

Create a test file `test_connection.py`:

```python
from app.database import engine
from sqlalchemy import text

try:
    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ MySQL connection successful!")
        print(f"Result: {result.fetchone()}")
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
```

Run it:
```bash
python test_connection.py
```

---

## Common Connection Issues

### Issue 1: "Can't connect to MySQL server"

**Causes:**
- MySQL server is not running
- Wrong host/port
- Firewall blocking connection

**Solutions:**
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Start MySQL if not running
sudo systemctl start mysql

# Check if port 3306 is listening
sudo netstat -tlnp | grep 3306
```

### Issue 2: "Access denied for user"

**Causes:**
- Wrong username or password
- User doesn't have privileges
- User can't connect from this host

**Solutions:**
```sql
-- Check if user exists
SELECT User, Host FROM mysql.user WHERE User = 'pg_user';

-- Grant privileges again
GRANT ALL PRIVILEGES ON pg_management_db.* TO 'pg_user'@'localhost';
FLUSH PRIVILEGES;
```

### Issue 3: "Unknown database"

**Causes:**
- Database doesn't exist
- Wrong database name

**Solutions:**
```sql
-- Check if database exists
SHOW DATABASES;

-- Create database if missing
CREATE DATABASE pg_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Issue 4: "Module 'pymysql' not found"

**Causes:**
- pymysql not installed

**Solutions:**
```bash
pip install pymysql
# OR
pip install -r requirements.txt
```

---

## Connection Pooling

The connection uses a pool to manage multiple connections efficiently:

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,        # Keep 10 connections ready
    max_overflow=20,     # Allow up to 20 extra connections
    pool_pre_ping=True   # Check connection before using
)
```

**Benefits:**
- Reuses connections instead of creating new ones
- Faster response times
- Better resource management

**Settings:**
- `pool_size=10`: Maintains 10 connections in the pool
- `max_overflow=20`: Can create up to 20 additional connections if needed
- `pool_pre_ping=True`: Verifies connection is alive before using (prevents stale connections)

---

## Debugging Connection Issues

### Enable SQL Query Logging

In `.env` file:
```env
DEBUG=True
```

This will log all SQL queries to console, helping you see what's happening.

### Check Connection String

Add this to your code temporarily:

```python
from app.config import settings
print(f"Database URL: {settings.DATABASE_URL.replace(settings.DATABASE_URL.split('@')[0].split('://')[1].split(':')[1], '***')}")
```

This prints the connection string (with password hidden) to verify it's correct.

---

## Complete Connection Flow Diagram

```
1. Application Starts
   ↓
2. app/config.py loads DATABASE_URL from .env
   ↓
3. app/database.py creates engine with connection string
   ↓
4. SQLAlchemy establishes connection pool to MySQL
   ↓
5. Request arrives at handler
   ↓
6. FastAPI calls get_db() dependency
   ↓
7. get_db() creates session from pool
   ↓
8. Handler uses session through repository
   ↓
9. Request completes
   ↓
10. get_db() closes session (returns to pool)
```

---

## Quick Setup Checklist

- [ ] MySQL server is installed and running
- [ ] Database `pg_management_db` is created
- [ ] User `pg_user` is created with password
- [ ] User has privileges on database
- [ ] `.env` file exists with correct `DATABASE_URL`
- [ ] `pymysql` is installed (`pip install -r requirements.txt`)
- [ ] Connection string format is correct
- [ ] Application starts without connection errors

---

## Example: Complete Setup

1. **Create .env file:**
```env
DATABASE_URL=mysql+pymysql://pg_user:my_password@localhost:3306/pg_management_db
SECRET_KEY=my-secret-key-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run application:**
```bash
python run.py
```

4. **Verify connection:**
- Check console for any errors
- Visit `http://localhost:8000/docs`
- Try creating a user via API

---

That's it! Your MySQL connection is now configured and working! 🎉

