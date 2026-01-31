# functions_app.py
# -*- coding: utf-8 -*-
import os
import streamlit as st
import requests

from src.auth_db import (
    authenticate,
    create_user,
    update_credentials
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def login_page():
    st.markdown("""
        <style>
            body {
                background-color: #f5f7fa;
            }

            .main-title {
                text-align: center;
                font-size: 36px;
                font-weight: 700;
                margin-top: 20px;
                color: #2c3e50;
            }

            .subtitle {
                text-align: center;
                font-size: 20px;
                color: #7f8c8d;
                margin-bottom: 10px;
            }

            .login-container {
                max-width: 420px;
                margin: 40px auto;
                padding: 30px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            .login-title {
                font-size: 26px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 20px;
                color: #34495e;
            }

            .info-text {
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 25px;
                font-size: 15px;
            }

            .stTextInput > div > div > input {
                border-radius: 8px;
            }

            .stButton > button {
                width: 100%;
                border-radius: 8px;
                background-color: #2ecc71;
                color: white;
                font-size: 16px;
                padding: 10px;
            }

            .stButton > button:hover {
                background-color: #27ae60;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">📦 DataCo Smart Supply Chain</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Decision Support Platform</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="login-container">
            <div class="login-title">🔐 Login</div>
            <div class="info-text">
                Welcome to the <b>DataCo Smart Supply Chain Platform</b>.<br>
                Monitor logistics performance, delivery risks and profitability.
            </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()

            # data contient seulement le token
            token = data.get("access_token")

            # 🔹 On récupère maintenant l'utilisateur complet via /me ou /get_user
            user_response = requests.get(
                f"{API_URL}/me",  # endpoint à créer qui renvoie id, role, first_login...
                headers={"Authorization": f"Bearer {token}"}
            )

            if user_response.status_code == 200:
                st.session_state.user = user_response.json()  # <-- stocke le dict complet
                st.session_state.token = token
                st.success("✅ Login successful")
                st.session_state.page = "home"
                st.rerun()           

            else:
                st.error("❌ Cannot fetch user info")

        else:
            st.error("❌ Incorrect username or password")

    st.markdown("</div>", unsafe_allow_html=True)



def first_login_page():
    st.markdown("""
        <style>
            .login-container {
                max-width: 420px;
                margin: 40px auto;
                padding: 30px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            .login-title {
                font-size: 26px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 20px;
                color: #34495e;
            }
            .stButton > button {
                width: 100%;
                border-radius: 8px;
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            .stButton > button:hover {
                background-color: #2980b9;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="login-container">
            <div class="login-title">🔄 First Login</div>
            <p style="text-align:center; color:#7f8c8d;">
                Please update your credentials to continue.
            </p>
    """, unsafe_allow_html=True)

    new_username = st.text_input("New username")
    new_password = st.text_input("New password", type="password")

    if st.button("Update credentials"):
        if not new_username or not new_password:
            st.error("⚠️ All fields are required.")
            st.stop()

        update_credentials(
            st.session_state.user["id"],
            new_username,
            new_password
        )

        st.success("✅ Credentials updated, please login again.")
        st.session_state.user = None
        st.session_state.page = "Login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def require_login():
    if "user" not in st.session_state or st.session_state.user is None:
        login_page()
        st.stop()

def page_managers():
    st.markdown("""
        <style>
            .manager-container {
                max-width: 520px;
                margin: 40px auto;
                padding: 30px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }

            .manager-title {
                font-size: 26px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 20px;
                color: #34495e;
            }

            .stTextInput > div > div > input {
                border-radius: 8px;
                padding: 8px;
            }

            .stButton > button {
                width: 100%;
                border-radius: 8px;
                font-size: 16px;
                padding: 10px;
                border: none;
            }

            .btn-create {
                background-color: #2ecc71 !important;
                color: white !important;
            }

            .btn-create:hover {
                background-color: #27ae60 !important;
            }

            .btn-cancel {
                background-color: #e74c3c !important;
                color: white !important;
            }

            .btn-cancel:hover {
                background-color: #c0392b !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="manager-container">
            <div class="manager-title">➕ Register a New Manager</div>
    """, unsafe_allow_html=True)

    first = st.text_input("First name")
    last = st.text_input("Last name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Temporary password", type="password")

    col_a, col_b = st.columns(2)

    with col_a:
        create_btn = st.button("Create", key="create_manager")
        if create_btn:
            if not last or not username or not email or not password:
                st.error("⚠️ Last name, username, email and password are required.")
                st.stop()

            if "@" not in email:
                st.error("⚠️ Invalid email format.")
                st.stop()

            headers = {"Authorization": f"Bearer {st.session_state.token}"}

            payload = {
                "first_name": first,
                "last_name": last,
                "username": username,
                "email": email,
                "password": password,
                "role": "manager"
            }

            response = requests.post(
                f"{API_URL}/create_user",
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                st.success("✅ Manager created successfully")
                st.session_state.page = "home"
                st.rerun()
            else:
                detail = response.json().get("detail", "Unknown error")
                st.error(f"❌ {detail}")

    with col_b:
        cancel_btn = st.button("Cancel", key="cancel_manager")
        if cancel_btn:
            st.session_state.page = "home"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <script>
            const buttons = window.parent.document.querySelectorAll('button[kind="secondary"]');
            if (buttons.length >= 2) {
                buttons[0].classList.add('btn-create');
                buttons[1].classList.add('btn-cancel');
            }
        </script>
    """, unsafe_allow_html=True)

def home_page():
    #st.set_page_config(page_title="🏠 Home - Smart Supply Chain Dashboard", layout="wide", page_icon="🏠")
    require_login()
    user = st.session_state.user
    role = user.get("role", "guest")

    # ---------- STYLE ----------
    st.markdown("""
        <style>
            body { background-color: #f4f6f9; }

            .home-container {
                max-width: 1000px;
                margin: 50px auto;
                padding: 50px;
                background: linear-gradient(145deg, #ffffff, #f1f3f6);
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            }

            .home-title {
                font-size: 42px;
                font-weight: 800;
                text-align: center;
                color: #1f2a44;
                margin-bottom: 10px;
            }

            .home-subtitle {
                font-size: 20px;
                text-align: center;
                color: #6c757d;
                margin-bottom: 40px;
            }

            .section { margin-top: 40px; }

            .section-title {
                font-size: 24px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 15px;
            }

            .section-text {
                font-size: 17px;
                line-height: 1.7;
                color: #4f5d73;
            }

            .highlight {
                color: #3498db;
                font-weight: 600;
            }

            .footer {
                margin-top: 60px;
                text-align: center;
                font-size: 14px;
                color: #95a5a6;
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------- CONTENU HTML ----------
    st.markdown("""
    <div class="home-container">
        <div class="home-title">📦 Smart Supply Chain Dashboard</div>
        <div class="home-subtitle">
            A Decision Support Platform for Order Performance & Logistics Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="home-container section">
        <div class="section-title">🚀 Application Overview</div>
        <div class="section-text">
            This platform is an advanced
            <span class="highlight">decision-support dashboard</span>
            designed to monitor, analyze, and optimize order performance across
            the supply chain.
            <br><br>
            It transforms logistics data into actionable insights to support
            strategic and operational decision-making.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- NAVIGATION (STREAMLIT ONLY) ----------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📦 Logistics"):
            st.session_state.page = "logistics"
            st.rerun()

    with col2:
        if st.button("📊 Overview"):
            st.session_state.page = "overview"
            st.rerun()

    with col3:
        if role == "patron":
            if st.button("👥 New Managers"):
                st.session_state.page = "Managers"
                st.rerun()
    with col4:
        if st.button("🚪 Log out"):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()

    # ---------- FOOTER ----------

    st.markdown("""
    <div class="home-container section">
        <div class="section-title">🧠 Project Designers</div>
        <div class="section-text">
            • <span class="highlight">MISSONGO Aimé Blanchard</span><br>
            • <span class="highlight">INGABIRE Crenia</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer">
            © 2025 — Smart Supply Chain Dashboard · AMSE
        </div>
    """, unsafe_allow_html=True)
