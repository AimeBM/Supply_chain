# pip install streamlit plotly streamlit-card pandas pydeck

import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from functions_app import require_login, login_page, page_managers

def render_over():
    require_login()
    # ✅ USER SAFE
    user = st.session_state.get("user", {})
    role = user.get("role")

    # --- CONFIG ---
    #st.set_page_config(page_title="Overview Dashboard", layout="wide", page_icon="📦")

    st.markdown("""
    <style>
    /* Réduire les marges globales */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 0.5rem;
    }

    /* Réduire l'espace entre sections */
    section[data-testid="stVerticalBlock"] > div {
        gap: 0.6rem;
    }

    /* Titres plus compacts */
    h1, h2, h3 {
        margin-bottom: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)


    # --- LOAD DATA ---
    df = pd.read_csv("data/processed/dataco_clean.csv") # Exemple si CSV
    # Ici on suppose que df est déjà chargé

    # --- APPLY FILTERS SAME AS LOGISTICS ---
    df_filtered = df.copy()  # ou appliquer les filtres globaux si besoin


    # --- HEADER ---

    st.title("📦 Overview Dashboard - Supply Chain Optimization")

    colA, colC, colB = st.columns(3)

    with colA:
        if role == "patron":
            if st.button("➕ Add Manager"):
                st.session_state.page = "Managers"
                st.rerun()

    with colC:
        if st.button("📦 Logistics"):
            st.session_state.page = "logistics"
            st.rerun()

    with colB:
        if user is not None:
            if st.button("🚪 Logout"):
                st.session_state.user = None
                st.rerun()
        else:
            st.warning("⚠️ You are not logged in.")
            login_page()
            st.stop()

    # =========================
    # 🎛️ OVERVIEW FILTERS
    # =========================

    with st.container(border=True):
        f1, f2, f3, f4 = st.columns(4)

        # 1️⃣ Order Status (Top 5)
        top_status = (
            df['Order Status']
            .value_counts()
            .head(5)
            .index
            .tolist()
        )

        with f1:
            status_filter = st.selectbox(
                "Order Status",
                ["All"] + top_status
            )

        # 2️⃣ Customer Segment
        with f2:
            segment_filter = st.selectbox(
                "Customer Segment",
                ["All"] + sorted(df['Customer Segment'].dropna().unique())
            )

        # 3️⃣ Category
        with f3:
            category_filter = st.selectbox(
                "Category",
                ["All"] + sorted(df['Category Name'].dropna().unique())
            )

        # 4️⃣ Time Period
        df['order_month'] = pd.to_datetime(
            df['order date (DateOrders)'],
            errors="coerce"
        ).dt.to_period("M").astype(str)

        with f4:
            period_filter = st.selectbox(
                "Time Period",
                ["All"] + sorted(df['order_month'].unique())
            )

    # =========================
    # APPLY FILTERS
    # =========================

    df_filtered = df.copy()

    if status_filter != "All":
        df_filtered = df_filtered[df_filtered['Order Status'] == status_filter]

    if segment_filter != "All":
        df_filtered = df_filtered[df_filtered['Customer Segment'] == segment_filter]

    if category_filter != "All":
        df_filtered = df_filtered[df_filtered['Category Name'] == category_filter]

    if period_filter != "All":
        df_filtered = df_filtered[df_filtered['order_month'] == period_filter]


    kpi_col, graph_col = st.columns([1.1, 2.2])

    # =========================
    # 🔹 KPIs (LEFT)
    # =========================

    overview_kpi_values = [
        f"${df_filtered['Sales'].sum():,.0f}",                          # Total Sales
        f"${df_filtered['order_profit'].sum():,.0f}",                   # Total Profit
        f"{df_filtered['profit_margin'].mean():.2f}%",                  # Profit Margin
        f"${df_filtered['Sales'].mean():,.0f}",                          # AOV
        f"{df_filtered['delivery_delay'].mean():.2f}",                  # Avg Delivery Delay
        f"{100 * (1 - df_filtered['is_late'].mean()):.2f}%",             # On-time %
        f"${df_filtered['order_profit'].mean():,.2f}",                  # Profit per Order
        f"{df_filtered['Order Item Discount Rate'].mean()*100:.2f}%",   # Discount Impact
        f"{df_filtered['Customer Id'].nunique():,}"                     # Unique Customers
    ]

    overview_kpi_labels = [
        "💰 Total Sales",
        "📈 Total Profit",
        "📊 Profit Margin",
        "🧾 Avg Order Value",
        "⏳ Avg Delivery Delay",
        "⚡ On-time Delivery",
        "💵 Profit per Order",
        "🏷 Discount Impact",
        "👥 Unique Customers"
    ]

    with kpi_col:
        # --- Première ligne de KPI ---
        with st.container():
            cols = st.columns(3)
            for i in range(3):
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:#f5f5f5; padding:15px; border-radius:20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); margin-bottom:10px;">
                        <div style="font-size:20px; font-weight:bold; color:#1f77b4;">{overview_kpi_values[i]}</div>
                        <div style="font-size:10px; margin-top:5px;">{overview_kpi_labels[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        # --- Petit espace entre les lignes ---
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Deuxième ligne de KPI ---
        with st.container(border=True):
            cols2 = st.columns(3)
            for i in range(3, 6):
                with cols2[i-3]:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:#f5f5f5; padding:15px; border-radius:20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); margin-bottom:10px;">
                        <div style="font-size:20px; font-weight:bold; color:#ff5722;">{overview_kpi_values[i]}</div>
                        <div style="font-size:10px; margin-top:5px;">{overview_kpi_labels[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)


        # ---   Troisième ligne de KPI ---
        with st.container():
            cols2 = st.columns(3)
            for i in range(6, 9):
                with cols2[i-6]:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:#f5f5f5; padding:15px; border-radius:20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); margin-bottom:10px;">
                        <div style="font-size:20px; font-weight:bold; color:#ff5722;">{overview_kpi_values[i]}</div>
                        <div style="font-size:10px; margin-top:5px;">{overview_kpi_labels[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.container():
            # Conversion en datetime
            df_filtered['order date (DateOrders)'] = pd.to_datetime(
                df_filtered['order date (DateOrders)'], errors='coerce'
            )
            df_filtered['shipping date (DateOrders)'] = pd.to_datetime(
                df_filtered['shipping date (DateOrders)'], errors='coerce'
            )

            # Comptage par Order Date
            orders_df = df_filtered.groupby(df_filtered['order date (DateOrders)'].dt.date).size().reset_index(name="Orders")
            orders_df['order_date_str'] = orders_df['order date (DateOrders)'].astype(str)

            # Comptage par Shipping Date
            shipped_df = df_filtered.groupby(df_filtered['shipping date (DateOrders)'].dt.date).size().reset_index(name="Shipped Orders")
            shipped_df['shipping_date_str'] = shipped_df['shipping date (DateOrders)'].astype(str)

            # Création du graphique avec deux traces indépendantes
            import plotly.graph_objects as go

            fig_time = go.Figure()

            # Orders (vert)
            fig_time.add_trace(go.Scatter(
                x=orders_df['order_date_str'],
                y=orders_df['Orders'],
                mode='lines+markers',
                name='Orders Placed',
                line=dict(color='green'),
                marker=dict(size=6)
            ))

            # Shipped Orders (rouge)
            fig_time.add_trace(go.Scatter(
                x=shipped_df['shipping_date_str'],
                y=shipped_df['Shipped Orders'],
                mode='lines+markers',
                name='Orders Shipped',
                line=dict(color='red'),
                marker=dict(size=6)
            ))

            # Layout compact et lisible
            fig_time.update_layout(
                title="Orders Placed vs Orders Shipped Over Time",
                xaxis_title="Date",
                yaxis_title="Number of Orders",
                height=260,
                margin=dict(t=40, b=10, l=10, r=10),
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_time, use_container_width=True)



    # =========================
    # 📈 GRAPHS (RIGHT)
    # =========================

    with graph_col:
        # -------- ROW 1 --------
        g1, g2, g3 = st.columns(3)

        # 1️⃣ Top 5 Category Profit
        with g1:
            cat_profit = (
                df_filtered.groupby("Category Name")["order_profit"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            fig_cat = px.bar(
                cat_profit,
                x="order_profit",
                y="Category Name",
                orientation="h",
                title="Top 5 Category Profit",
                text_auto=".2s",
                color="order_profit",
                color_continuous_scale="Blues"
            )
            fig_cat.update_layout(height=300, margin=dict(t=40, b=10), coloraxis_showscale=False)
            st.plotly_chart(fig_cat, use_container_width=True)

        # 2️⃣ Sales by Customer Segment (Donut)
        with g2:
            seg_sales = (
                df_filtered.groupby("Customer Segment")["Sales"]
                .sum()
                .reset_index()
            )

            fig_seg = px.pie(
                seg_sales,
                names="Customer Segment",
                values="Sales",
                hole=0.6,
                title="Sales by Segment"
            )
            fig_seg.update_traces(
                textinfo='percent',
                textposition='inside',
                insidetextfont=dict(size=10)
            )
            fig_seg.update_layout(
                height=260, margin=dict(t=40, b=30),
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=8)
                ))
            st.plotly_chart(fig_seg, use_container_width=True)

        # 3️⃣ Average Sales per Day
        with g3:
            # Convertir en datetime
            df_filtered['order date (DateOrders)'] = pd.to_datetime(df_filtered['order date (DateOrders)'], errors='coerce')

            daily_sales = (
                df_filtered
                .groupby(df_filtered["order date (DateOrders)"].dt.date)["Sales"]
                .mean()
                .reset_index()
            )

            fig_day = px.line(
                daily_sales,
                x="order date (DateOrders)",
                y="Sales",
                title="Average Sales per Day"
            )
            fig_day.update_layout(height=280, margin=dict(t=40, b=10))
            st.plotly_chart(fig_day, use_container_width=True)

        # -------- ROW 2 --------
        g4, g5, g6 = st.columns(3)

        # 4️⃣ Order Status Distribution
        with g4:
            status_df = (
                df_filtered
                .groupby("Order Status")
                .agg(
                    Orders=("Order Id", "nunique"),
                    Sales=("Sales", "sum"),
                    Profit=("order_profit", "sum")
                )
                .sort_values("Orders", ascending=False)
                .head(5)
                .reset_index()
            )
            fig_status = px.treemap(
                status_df,
                path=["Order Status"],
                values="Orders",              # 👈 valeur principale
                color="Profit",               # 👈 performance
                title="Order Status Distribution (by Orders)",
                hover_data={
                    "Orders": ":,.0f",
                    "Sales": ":,.0f",
                    "Profit": ":,.0f"
                }
            )
            fig_status.update_layout(
                height=260,
                margin=dict(t=40, b=10, l=10, r=10),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_status, use_container_width=True)

        # 5️⃣ Top Order States
        with g5:
            state_df = (
                df_filtered['Order State']
                .value_counts()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            state_df.columns = ["State", "Orders"]

            fig_state = px.bar(
                state_df,
                x="Orders",
                y="State",
                orientation="h",
                title="Top Order States",
                text_auto=True
            )
            fig_state.update_layout(height=260, margin=dict(t=40, b=10))
            st.plotly_chart(fig_state, use_container_width=True)

        # 6️⃣ Top Customer Cities
        with g6:
            city_df = (
                df_filtered['Customer City']
                .value_counts()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            city_df.columns = ["City", "Orders"]

            fig_city = px.bar(
                city_df,
                x="City",
                y="Orders",
                title="Top Customer Cities",
                text_auto=True
            )

            fig_city.update_layout(height=260, margin=dict(t=40, b=10))
            st.plotly_chart(fig_city, use_container_width=True)

render_over()