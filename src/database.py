import sqlite3

DB_FILE = "keymorpher.db"

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
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

def insert_user(name, roll, branch):
    """Inserts a new user record into the database."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, roll, branch)
                VALUES (?, ?, ?)
            ''', (name, roll, branch))
            conn.commit()
            print("User data saved successfully")
    except sqlite3.Error as e:
        print(f"Database insert error: {e}")
