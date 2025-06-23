import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from db import init_all_databases, delete_old_guest_entries

# Initialize DBs
init_all_databases()

# Load credentials
import os
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set up authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# Login form
authenticator.login(
    location='main',
    fields={"Form name": "Login"}
)

# Handle auth
if "user" not in st.session_state:
    st.session_state["user"] = None
    
auth_status = st.session_state.get("authentication_status")

if auth_status is False:
    st.error("Username/password is incorrect.")
    st.stop()

elif auth_status is None:
    st.warning("Welcome back! Log in to generate content instantly.")
    if st.button("🔒 Continue as Guest"):
        st.session_state["user"] = "guest"
    else:
        st.stop()

if auth_status:
    st.session_state["user"] = st.session_state.get("username", "unknown")
    st.sidebar.write(f"Welcome, *{st.session_state.get('name', 'User')}*")
    authenticator.logout("Logout", "sidebar")

if st.session_state.get("user") == "guest":
    delete_old_guest_entries(hours=1)
