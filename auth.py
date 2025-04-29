import sqlite3
import streamlit as st
from hashlib import sha256
from datetime import datetime

DB = "users.db"

def init_user_db():
    connection = sqlite3.connect(DB)
    c = connection.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TEXT
        )
    ''')
    connection.commit()
    connection.close()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                  (username, hash_password(password), datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def auth_tabs():
    tab1, tab2 = st.tabs(["🔐 Sign In", "🆕 Sign Up"])

    with tab1:
        st.markdown("Welcome back! Log in to generate content instantly.")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.user = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.markdown("🆕 New to AI Content Generator? Sign up now to get started.")
        new_user = st.text_input("Choose a username", key="signup_user")
        new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if create_user(new_user, new_pass):
                # If they were a Guest before
                if st.session_state.get("guest_id"):
                    conn = sqlite3.connect("guests.db")
                    c = conn.cursor()
                    c.execute('UPDATE guest_sessions SET converted = 1 WHERE guest_id = ?', (st.session_state.guest_id,))
                    conn.commit()
                    conn.close()

                st.success("Account created! You can now log in.")
            else:
                st.error("Username already exists.")
    
    # Guest Login Option 
    st.markdown("---")
    st.markdown("👋 Want to try it without signing up?")
    if st.button("🔓 Continue as Guest"):
        guest_id = str(datetime.utcnow().timestamp())  # simple guest id
        st.session_state.guest_id = guest_id
        st.session_state.user = "guest"

        # Save guest session
        conn = sqlite3.connect("guests.db")
        c = conn.cursor()
        c.execute('INSERT INTO guest_sessions (guest_id, created_at) VALUES (?, ?)', 
                (guest_id, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()

        st.success("You're logged in as a Guest!")
        st.rerun()



def logout_button():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()

def is_logged_in():
    return st.session_state.get("user") is not None
