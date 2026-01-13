# Setting Up Database with MySQL Workbench

This guide shows you how to create the database and user for the PG Management System using MySQL Workbench.

---

## Prerequisites

- MySQL Server installed and running
- MySQL Workbench installed
- MySQL Server accessible

---

## Step 1: Open MySQL Workbench

1. Launch MySQL Workbench from your applications menu
2. You'll see the MySQL Workbench interface

---

## Step 2: Connect to MySQL Server

1. In the **"MySQL Connections"** section, you should see a connection (usually named "Local instance MySQL" or similar)
2. Click on the connection to open it
3. Enter your MySQL root password when prompted
4. Click **"OK"**

**If you don't have a connection set up:**
1. Click the **"+"** button next to "MySQL Connections"
2. Fill in the connection details:
   - **Connection Name**: `PG Management Server` (or any name)
   - **Hostname**: `127.0.0.1` or `localhost`
   - **Port**: `3306` (default MySQL port)
   - **Username**: `root`
   - **Password**: Click **"Store in Keychain"** and enter your MySQL root password
3. Click **"Test Connection"** to verify
4. Click **"OK"** to save
5. Double-click the connection to connect

---

## Step 3: Create Database

### Method 1: Using SQL Query (Recommended)

1. Once connected, you'll see the SQL Editor
2. In the query editor, type:
   ```sql
   CREATE DATABASE pg_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Click the **"Execute"** button (lightning bolt icon) or press `Ctrl+Enter`
4. You should see "Success" in the output panel

### Method 2: Using GUI

1. In the left sidebar, right-click on **"Schemas"**
2. Select **"Create Schema..."**
3. In the **"Schema Name"** field, enter: `pg_management_db`
4. In **"Charset"** dropdown, select: `utf8mb4`
5. In **"Collation"** dropdown, select: `utf8mb4_unicode_ci`
6. Click **"Apply"**
7. Review the SQL script and click **"Apply"** again
8. Click **"Finish"**

✅ Database `pg_management_db` is now created!

---

## Step 4: Create User

1. In the SQL Editor, run the following command:
   ```sql
   CREATE USER 'pg_user'@'localhost' IDENTIFIED BY 'your_password_here';
   ```
   **Important:** Replace `your_password_here` with a strong password (remember this!)

2. Click **"Execute"** (or press `Ctrl+Enter`)

✅ User `pg_user` is now created!

---

## Step 5: Grant Privileges to User

1. In the SQL Editor, run these commands one by one:

```sql
-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON pg_management_db.* TO 'pg_user'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
```

2. Click **"Execute"** after each command

**Alternative - Grant specific privileges:**
```sql
-- Grant specific privileges (more secure)
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER 
ON pg_management_db.* TO 'pg_user'@'localhost';

FLUSH PRIVILEGES;
```

✅ User `pg_user` now has full access to `pg_management_db`!

---

## Step 6: Verify User and Privileges

1. Run this query to verify the user was created:
   ```sql
   SELECT User, Host FROM mysql.user WHERE User = 'pg_user';
   ```

2. Run this query to verify privileges:
   ```sql
   SHOW GRANTS FOR 'pg_user'@'localhost';
   ```

You should see the privileges listed.

---

## Step 7: Test Connection with New User

1. In MySQL Workbench, create a new connection:
   - Click the **"+"** button
   - **Connection Name**: `PG Management DB`
   - **Hostname**: `127.0.0.1` or `localhost`
   - **Port**: `3306`
   - **Username**: `pg_user`
   - **Password**: Click **"Store in Keychain"** and enter the password you set
   - **Default Schema**: `pg_management_db`
2. Click **"Test Connection"**
3. If successful, click **"OK"** and connect using this new connection

---

## Step 8: Update .env File

Create or update your `.env` file in the project root:

```env
# Database Configuration (MySQL)
DATABASE_URL=mysql+pymysql://pg_user:YOUR_PASSWORD_HERE@localhost:3306/pg_management_db

# Format: mysql+pymysql://username:password@host:port/database_name

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Important:** 
- Replace `YOUR_PASSWORD_HERE` with the actual password you set for `pg_user` in Step 4
- The connection string uses `mysql+pymysql://` (not just `mysql://`)

---

## Step 9: Install Python Dependencies

Make sure you have the MySQL driver installed:

```bash
pip install -r requirements.txt
```

This will install `pymysql` which is the MySQL driver for Python.

---

## Step 10: Test Database Connection

Run your application:

```bash
python run.py
```

The application will:
1. Connect to the MySQL database
2. Create tables automatically (if using `Base.metadata.create_all()`)
3. Start the server

---

## Viewing Tables in MySQL Workbench

After running your application, you can view the created tables:

1. In MySQL Workbench, expand `pg_management_db` in the left sidebar
2. Expand **"Tables"**
3. You should see the `users` table (and others as you add features)
4. Right-click on a table → **"Select Rows - Limit 1000"** to view data

---

## Troubleshooting

### Issue: "Access denied for user"
- **Solution**: 
  - Verify the password in `.env` matches the password you set
  - Check if user exists: `SELECT User FROM mysql.user WHERE User = 'pg_user';`
  - Re-grant privileges if needed

### Issue: "Unknown database"
- **Solution**: 
  - Verify database name in `.env` matches: `pg_management_db`
  - Check if database exists: `SHOW DATABASES;`

### Issue: "Can't connect to MySQL server"
- **Solution**: 
  - Check if MySQL service is running: `sudo systemctl status mysql`
  - Start MySQL if not running: `sudo systemctl start mysql`
  - Verify port 3306 is not blocked by firewall

### Issue: "pymysql module not found"
- **Solution**: 
  ```bash
  pip install pymysql
  # OR
  pip install -r requirements.txt
  ```

### Issue: "Authentication plugin error"
- **Solution**: 
  - MySQL 8.0+ uses `caching_sha2_password` by default
  - Change user authentication:
    ```sql
    ALTER USER 'pg_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
    FLUSH PRIVILEGES;
    ```

---

## Quick Reference

| Item | Value |
|------|-------|
| Database Name | `pg_management_db` |
| Username | `pg_user` |
| Password | (The one you set) |
| Host | `localhost` or `127.0.0.1` |
| Port | `3306` |
| Connection String | `mysql+pymysql://pg_user:PASSWORD@localhost:3306/pg_management_db` |

---

## SQL Commands Summary

Here are all the SQL commands you need (run in MySQL Workbench):

```sql
-- 1. Create database
CREATE DATABASE pg_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Create user
CREATE USER 'pg_user'@'localhost' IDENTIFIED BY 'your_password_here';

-- 3. Grant privileges
GRANT ALL PRIVILEGES ON pg_management_db.* TO 'pg_user'@'localhost';

-- 4. Apply changes
FLUSH PRIVILEGES;

-- 5. Verify (optional)
SELECT User, Host FROM mysql.user WHERE User = 'pg_user';
SHOW GRANTS FOR 'pg_user'@'localhost';
```

---

## Alternative: Using MySQL Command Line

If you prefer command line:

```bash
# Connect to MySQL
mysql -u root -p

# Then run the SQL commands:
CREATE DATABASE pg_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pg_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON pg_management_db.* TO 'pg_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## Next Steps

Once your database is set up:

1. ✅ Update `.env` file with MySQL connection details
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Run the application: `python run.py`
4. ✅ Tables will be created automatically on first run
5. ✅ Test the API at `http://localhost:8000/docs`

---

## Connection Details

| Feature | MySQL |
|---------|-------|
| Port | 3306 |
| Connection String | `mysql+pymysql://...` |
| Driver | `pymysql` |
| Default Charset | utf8mb4 (recommended) |

That's it! Your MySQL database is ready to use with MySQL Workbench. 🎉

