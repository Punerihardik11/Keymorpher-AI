#!/usr/bin/env python3
"""
Database Viewer Script - Shows all user data collected by Keymorpher AI
Perfect for demonstrating data persistence to teachers
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "keymorpher.db")

def view_database():
    """Display all user records in a clean table format"""
    
    print("\n" + "=" * 90)
    print("KEYMORPHER AI - DATABASE VIEWER")
    print("=" * 90)
    print(f"Database Location: {DB_FILE}\n")
    
    if not os.path.exists(DB_FILE):
        print("[ERROR] Database file not found!")
        print(f"        Expected at: {DB_FILE}")
        print("\n[INFO] The database is created when the application runs for the first time.")
        print("       Steps to see data:")
        print("       1. Run: python src/main.py")
        print("       2. Enter name, roll number, and branch data")
        print("       3. Exit the application")
        print("       4. Run this script again: python view_database.py\n")
        return False
    
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                print("[ERROR] Users table not found in database!\n")
                return False
            
            # Get all records
            cursor.execute("SELECT id, name, roll, branch, created_at FROM users ORDER BY id ASC")
            records = cursor.fetchall()
            
            if not records:
                print("[INFO] No records found in database yet.")
                print("       Run the application first to collect data.\n")
                return False
            
            # Display header
            print("[OK] Found {} record(s) in database:\n".format(len(records)))
            
            # Display in table format
            print(f"{'ID':<4} | {'Name':<25} | {'Roll Number':<12} | {'Branch':<8} | {'Date & Time':<19}")
            print("-" * 90)
            
            for record_id, name, roll, branch, timestamp in records:
                # Format timestamp for better readability
                try:
                    dt = datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp
                
                # Ensure name doesn't overflow
                name_display = name[:25] if len(name) > 25 else name
                
                print(f"{record_id:<4} | {name_display:<25} | {roll:<12} | {branch:<8} | {formatted_time:<19}")
            
            print("-" * 90)
            
            # Summary statistics
            print(f"\n[SUMMARY]")
            print(f"  Total Records: {len(records)}")
            
            # Count by branch
            cursor.execute("SELECT branch, COUNT(*) FROM users GROUP BY branch ORDER BY branch ASC")
            branch_stats = cursor.fetchall()
            
            if branch_stats:
                print(f"\n  Records by Branch:")
                for branch, count in branch_stats:
                    print(f"    • {branch}: {count} record(s)")
            
            # Date range
            cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM users")
            min_date, max_date = cursor.fetchone()
            
            print(f"\n  First Entry: {min_date}")
            print(f"  Last Entry:  {max_date}")
            
            print("\n" + "=" * 90)
            print("[SUCCESS] Data successfully retrieved from database!")
            print("=" * 90 + "\n")
            
            return True
            
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}\n")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}\n")
        return False

if __name__ == "__main__":
    view_database()
