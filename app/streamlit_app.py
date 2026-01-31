import streamlit as st

from src.auth_db import (
    init_db,
    authenticate,
    create_user,
    update_credentials
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="DataCo Smart Supply Chain",
    layout="centered"
)

# -----------------------------------
# SESSION STATE INIT
# -----------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -----------------------------------
# HEADER
# -----------------------------------
if st.session_state.user is not None:

    st.markdown("""
    <div class="app-header">
        <div class="header-left">
            📦 <span>DataCo Smart Supply Chain</span>
        </div>
        <div class="header-right" id="header-buttons">
        </div>
    </div>

    <style>
    .app-header {
        top: 48px;
        left: 0;
        right: 0;
        height: 70px;
        background: linear-gradient(90deg, #0b1f3a, #102a4d);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        z-index: 999;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
        color: white;
        font-size: 20px;
        font-weight: 700;
    }

    .header-right {
        display: flex;
        gap: 12px;
        align-items: center;
    }

    .block-container {
        padding-top: 140px;
    }
    </style>
    """, unsafe_allow_html=True)


if st.session_state.user is not None:
    colA, colB = st.columns(2)

    with colA:
        if st.session_state.user["role"] == "patron":
            add_manager = st.button("➕ Add Manager")

    with colB:
        logout = st.button("🚪 Logout")
    # Actions
    if st.session_state.user["role"] == "patron" and add_manager:
        st.session_state.show_add_manager = True

    if logout:
        st.session_state.user = None
        st.rerun()


# -----------------------------------
# INIT DATABASE
# -----------------------------------
init_db()

# -----------------------------------
# LOGIN / FIRST LOGIN / POST LOGIN
# -----------------------------------

# ---- LOGIN PAGE ----
if st.session_state.user is None:
    st.title("📦 DataCo Smart Supply Chain")
    st.subheader("Decision Support Platform")
    st.markdown("---")

    st.markdown(
        """
        Welcome to the **DataCo Smart Supply Chain Platform**.  
        This tool helps decision-makers monitor **logistics performance,
        delivery risks and profitability** using Big Data.
        """
    )

    # Card login
    st.markdown(
        """
        <div class="login-card">
            <div class="login-title">🔐 Login</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("❌ Incorrect username or password")

    st.markdown(
        """
        <style>
        /* Global background stays white */
        .stApp {
            background-color: #ffffff;
        }

        /* Center card */
        .login-card {
            background-color: #0b1f3a;
            border-radius: 18px;
            font-size: 40px;
            box-shadow: 0px 15px 40px rgba(0, 60, 120, 0.25);
            color: white;
            padding: 25px;
            margin-top: 20px;
        }

        /* Inputs */
        .login-card input {
            border-radius: 8px !important;
        }

        /* Button */
        .login-card .stButton>button {
            width: 100%;
            background-color: #1e88e5;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            font-weight: 600;
            border: none;
        }

        .login-card .stButton>button:hover {
            background-color: #1565c0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# ---- FIRST LOGIN ----
if st.session_state.user["first_login"] == 1:
    st.warning("⚠️ First login – please update your credentials")

    new_username = st.text_input("New username")
    new_password = st.text_input("New password", type="password")

    if st.button("Update credentials"):
        update_credentials(
            st.session_state.user["id"],
            new_username,
            new_password
        )
        st.success("✅ Credentials updated, please login again.")
        st.session_state.user = None
        st.rerun()
    st.stop()

if st.session_state.get("show_add_manager", False):
    st.markdown("### ➕ Register a new manager")

    first = st.text_input("First name")
    last = st.text_input("Last name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Temporary password", type="password")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Create"):
            create_user(first, last, username, email, password, "manager")
            st.success("✅ Manager created successfully")
            st.session_state.show_add_manager = False

    with col_b:
        if st.button("Cancel"):
            st.session_state.show_add_manager = False


