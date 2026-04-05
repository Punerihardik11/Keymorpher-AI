import sqlite3
import os

# Use absolute path for database - works regardless of where script is run from
DB_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(os.path.dirname(DB_DIRECTORY), "keymorpher.db")

def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll TEXT NOT NULL,
                    branch TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print(f"[OK] Database initialized at: {DB_FILE}")
    except sqlite3.Error as e:
        print(f"[ERROR] Database initialization error: {e}")
        raise

def insert_user(name, roll, branch):
    """Inserts a new user record into the database with validation."""
    # Validate inputs
    if not name or not roll or not branch:
        print("[ERROR] Cannot save empty fields to database")
        return False
    
    if len(str(name).strip()) < 2:
        print("[ERROR] Name is too short (minimum 2 characters)")
        return False
        
    if len(str(roll).strip()) < 1:
        print("[ERROR] Roll number cannot be empty")
        return False
    
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, roll, branch)
                VALUES (?, ?, ?)
            ''', (name.strip(), roll.strip(), branch.strip()))
            conn.commit()
            print(f"[OK] User data saved successfully: {name} | {roll} | {branch}")
            return True
    except sqlite3.Error as e:
        print(f"[ERROR] Database insert error: {e}")
        return False
