import sqlite3
import datetime
import hashlib
import streamlit as st
import pandas as pd
DATABASE_PATH='database/mental_health.db'

def create_table():
    # Connect to an SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('database/mental_health.db')
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS mental_health 
             (date TEXT, feeling integer, serenity integer, sleep integer, productivity integer, enjoyment integer, average real,username TEXT NOT NULL)''')
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()

def add_entry(date: str,feeling: int,serenity: int,sleep: int,productivity: int,enjoyment: int,average: float):
    conn = sqlite3.connect('database/mental_health.db')
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    
    #cursor.execute("INSERT INTO mental_health VALUES ({date},{feeling},{serenity},{sleep},{productivity},{enjoyment},{average})".format(date='2024-11-13',
    #    feeling=feeling,serenity=serenity,sleep=sleep,productivity=productivity,enjoyment=enjoyment,average=average))

    cursor.execute("INSERT INTO mental_health VALUES (?,?,?,?,?,?,?,?)",(date,feeling,serenity,sleep,productivity,enjoyment,average,st.session_state.get("current_user", None)))    
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()

def get_usertable_conn():
    conn = sqlite3.connect(DATABASE_PATH)  # Replace with your database file
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password_hash TEXT)''')
    return conn


# Hash a password for storing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
def register_user(username, password):
    conn = get_usertable_conn()
    password_hash = hash_password(password)
    try:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    finally:
        conn.close()

# Validate login
def validate_user(username, password):
    conn = get_usertable_conn()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user is not None
    
def validate_username(username):
    conn = get_usertable_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Register a new user
def delete_user(username):
    conn = get_usertable_conn()
    #password_hash = hash_password(password)
    try:
        conn.execute("DELETE FROM users WHERE username = ?", (username))
        conn.commit()
    except :
        print("User name not found")
        st.error("Username Not Found.")
    finally:
        conn.close()
        
# Register a new user
def show_users():
    conn = get_usertable_conn()
    #password_hash = hash_password(password)
    try:
        #DELETE FROM artists_backup WHERE artistid = 1;
        #conn.execute("SELECT * FROM users ORDER BY username ASC")
        df = pd.read_sql_query("SELECT * FROM users ORDER BY username ASC", conn)
        st.dataframe(df)
        #conn.commit()
    except sqlite3.IntegrityError:
        st.error("Error getting user")
    finally:
        conn.close()

def create_activity_table():
    conn = sqlite3.connect('database/mental_health.db')
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS activities 
             (date TEXT, activity_name TEXT, duration int,username TEXT NOT NULL)''')
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()
    
def log_activity(date,activity,duration):
    conn = sqlite3.connect('database/mental_health.db')
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    print(type(date))
    #cursor.execute("INSERT INTO mental_health VALUES ({date},{feeling},{serenity},{sleep},{productivity},{enjoyment},{average})".format(date='2024-11-13',
    #    feeling=feeling,serenity=serenity,sleep=sleep,productivity=productivity,enjoyment=enjoyment,average=average))

    cursor.execute("INSERT INTO activities VALUES (?,?,?,?)",(date,activity,duration,st.session_state.get("current_user", None)))    
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()
