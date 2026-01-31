import os
import streamlit as st

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth_db import init_db
from functions_app import login_page, first_login_page, page_managers

# Au début du fichier Streamlit, avant toute requête
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")



st.set_page_config(
    page_title="DataCo Smart Supply Chain",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

# ---------------- INIT ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- AUTH ----------------
if st.session_state.page == "Login":
    from functions_app import login_page
    login_page()
    st.stop()

if st.session_state.user and st.session_state.user.get("first_login", 0) == 1:
    from functions_app import first_login_page
    first_login_page()
    st.stop()

# ---------------- ROUTING ----------------
if st.session_state.page == "home":
    from functions_app import home_page
    home_page()
    st.stop()

st.session_state.page = "home" # for erro of last time, we deactivate all pages

if st.session_state.page == "overview":
    from pages.overview import render_over
    render_over()
    st.stop()

if st.session_state.page == "logistic":
    from pages.logistic import render_log
    render_log()
    st.stop()

if st.session_state.page == "Managers":
    from functions_app import page_managers
    page_managers()
    st.stop()
