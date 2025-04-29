import streamlit as st

# demol
USERS = {
    "admin": "admin123",
    "demo": "demo123"
}

def login_form():
    st.subheader("🔐 Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.user = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

def logout_button():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()

def is_logged_in():
    return st.session_state.get("user") is not None

def signup_form():
    st.subheader("🆕 Sign Up")
    st.info("Signup is disabled in demo. Add new users in `auth.py`.")
