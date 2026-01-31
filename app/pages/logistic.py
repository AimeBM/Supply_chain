# pip install streamlit plotly streamlit-card pandas pydeck

import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

from functions_app import require_login, login_page, page_managers

def render_log():
    require_login()

    # ✅ USER SAFE
    user = st.session_state.get("user", {})
    role = user.get("role")
    # --- CONFIG ---
    #st.set_page_config(page_title="🚚 Logistics Dashboard", layout="wide", page_icon="📦")

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

    # --- HEADER ---

    st.title("📦 Logistics Dashboard - Supply Chain Optimization")
    colA, colC, colB = st.columns(3)

    with colA:
        if role == "patron":
            if st.button("➕ Add Manager"):
                st.session_state.page = "Managers"
                st.stop()

    with colC:
        if st.button("📊 Overview"):
            st.session_state.page = "overview"
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


    # --- FILTER CONTAINER ---
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            country_filter = st.selectbox("Customer Country", options=["All"] + list(df['Customer Country'].unique()))
        with col2:
            shipping_filter = st.selectbox("Shipping Mode", options=["All"] + list(df['Shipping Mode'].unique()))
        with col3:
            segment_filter = st.selectbox("Customer Segment", options=["All"] + list(df['Customer Segment'].unique()))
        with col4:
            # Convertir en datetime
            df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')

            # Créer colonne année-mois pour le filtre
            df['order_month_year'] = df['order date (DateOrders)'].dt.to_period('M')
            period_filter = st.selectbox("Order Time Period", options=["All"] + list(df['order_month_year'].astype(str).unique()))

    # --- APPLY FILTERS ---
    df_filtered = df.copy()
    if country_filter != "All":
        df_filtered = df_filtered[df_filtered['Customer Country'] == country_filter]
    if shipping_filter != "All":
        df_filtered = df_filtered[df_filtered['Shipping Mode'] == shipping_filter]
    if segment_filter != "All":
        df_filtered = df_filtered[df_filtered['Customer Segment'] == segment_filter]
    if period_filter != "All":
        df_filtered = df_filtered[df_filtered['order_month_year'].astype(str) == period_filter]

    # --- KPIs LOGISTIQUES COMPACTES ---
    kpi_values = [
        f"{df_filtered['Order Id'].nunique():,}",
        f"{df_filtered['real_shipping_days'].mean():.2f}",
        f"{df_filtered['delivery_delay'].mean():.2f}",
        f"{100*(1-df_filtered['is_late'].mean()):.2f}%",
        f"{df_filtered['is_late'].sum():,}",
        f"{df_filtered['Order Id'].sum():,}",
        f"{df_filtered['order_processing_days'].mean():.2f}",
        f"{df_filtered['Customer City'].nunique():,}",
        f"{df_filtered['late_risk'].mean():.2f}"
    ]

    kpi_labels = [
        " Orders Shipped",
        "⏱ Avg Shipping Days",
        "⏳ Avg Delay Days",
        "⚠️ On-time %",
        "🚨 Delayed Products",
        "📦 Total Products",
        "⏱ Avg Processing Days",
        "🏙 Customer Cities",
        "📊 Avg Late Risk"
    ]

    kpi_col, graph_col = st.columns([1.1, 2.2])

    with kpi_col:
    # --- Première ligne de KPI ---
        with st.container(border=True):
            cols = st.columns(3)
            for i in range(3):
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:#f5f5f5; padding:15px; border-radius:20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); margin-bottom:10px;">
                        <div style="font-size:20px; font-weight:bold; color:#1f77b4;">{kpi_values[i]}</div>
                        <div style="font-size:10px; margin-top:5px;">{kpi_labels[i]}</div>
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
                        <div style="font-size:20px; font-weight:bold; color:#ff5722;">{kpi_values[i]}</div>
                        <div style="font-size:10px; margin-top:5px;">{kpi_labels[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)


        # ---   Troisième ligne de KPI ---
        with st.container(border=True):
            cols2 = st.columns(3)
            for i in range(6, 9):
                with cols2[i-6]:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:#f5f5f5; padding:15px; border-radius:20px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); margin-bottom:10px;">
                        <div style="font-size:20px; font-weight:bold; color:#ff5722;">{kpi_values[i]}</div>
                        <div style="font-size:10px; margin-top:5px;">{kpi_labels[i]}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with graph_col:
        g1, g2, g3 = st.columns(3)

        # 1️⃣ Delivery Status (donut – legend bottom, % visible)
        with g1:
            status_df = df_filtered['Delivery Status'].value_counts().reset_index()
            status_df.columns = ['Status', 'Count']

            fig_status = px.pie(
                status_df,
                names='Status',
                values='Count',
                hole=0.6,
                title="Delivery Status",
                color='Status'
            )

            fig_status.update_traces(
                textinfo='percent',
                textposition='inside',
                insidetextfont=dict(size=10)
            )

            fig_status.update_layout(
                height=260,
                margin=dict(t=35, b=40, l=10, r=10),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=8)
                )
            )

            st.plotly_chart(fig_status, use_container_width=True)


        # 2️⃣ Delivery by Customer City (horizontal bar)
        with g2:
            city_df = (
                df_filtered['Customer City']
                .value_counts()
                .head(10)
                .reset_index()
            )
            city_df.columns = ['City', 'Shipments']

            fig_city = px.bar(
                city_df,
                x='Shipments',
                y='City',
                orientation='h',
                title="Top 10 Delivery Cities",
                text='Shipments',
                color='Shipments',
                color_continuous_scale='Blues'
            )

            fig_city.update_layout(
                height=260,
                margin=dict(t=40, b=10, l=10, r=10),
                yaxis=dict(autorange="reversed"),  # plus gros en haut
                coloraxis_showscale=False
            )

            fig_city.update_traces(
                textposition='outside',
                textfont_size=11
            )

            st.plotly_chart(fig_city, use_container_width=True)


        # 3️⃣ Orders Density Map (replaces Fleet Load)
        map_df = (
        df_filtered
        .groupby(['Customer City', 'Customer Country', 'Latitude', 'Longitude'])
        .agg(
            Shipments=('Order Id', 'count'),
            Total_Sales=('Sales', 'sum'),
            Late_Rate=('is_late', 'mean')
        )
        .reset_index()
        )

        # arrondir le Late_Rate en pourcentage et total sales à 2 décimales
        map_df['Late_Rate'] = (map_df['Late_Rate'] * 100).round(2).astype(str) + '%'
        map_df['Total_Sales'] = map_df['Total_Sales'].round(2)

        # 3️⃣ Logistics Orders Density Map (compact, replaces Fleet Load)
        with g3:  # remplace Fleet Load
            mid_lat = map_df['Latitude'].mean()
            mid_lon = map_df['Longitude'].mean()

            deck = pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v10",
                initial_view_state=pdk.ViewState(
                    latitude=mid_lat,
                    longitude=mid_lon,
                    zoom=2.8,
                    pitch=35
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=map_df,
                        get_position='[Longitude, Latitude]',
                        get_radius='Shipments * 300',
                        get_fill_color='[200, 30, 0, 140]',
                        pickable=True
                    )
                ],
                tooltip={
                    "html": """
                    <b>City:</b> {Customer City}<br/>
                    <b>Country:</b> {Customer Country}<br/>
                    <b>Shipments:</b> {Shipments}<br/>
                    <b>Sales:</b> ${Total_Sales}<br/>
                    <b>Late Rate:</b> {Late_Rate}
                    """,
                    "style": {
                    "backgroundColor": "white",
                    "color": "black",
                    "fontSize": "11px"
                }
                }
            )

            st.pydeck_chart(deck, use_container_width=True, height=260)


        g5, g6 = st.columns(2)
        # 5️⃣ Delay by Shipping Mode
        with g5:
            mode_df = df_filtered.groupby('Shipping Mode')['delivery_delay'].mean().reset_index()

            fig_mode = px.bar(
                mode_df,
                x='Shipping Mode',
                y='delivery_delay',
                title="Avg Delay by Shipping Mode"
            )
            fig_mode.update_layout(height=260, margin=dict(t=40, b=10))
            st.plotly_chart(fig_mode, use_container_width=True)

        # 6️⃣ Orders Over Time (by Shipping Date)
        with g6:
            # Conversion en datetime
            df_filtered['shipping date (DateOrders)'] = pd.to_datetime(
                df_filtered['shipping date (DateOrders)'],
                errors='coerce'
            )

            # Comptage des commandes par date d'expédition
            time_df = (
                df_filtered
                .groupby(df_filtered['shipping date (DateOrders)'].dt.date)
                .size()
                .reset_index(name="Orders Shipped")
            )

            # Convertir la date en string pour Plotly
            time_df['shipping date (DateOrders)'] = time_df['shipping date (DateOrders)'].astype(str)

            # Ligne avec markers
            fig_time = px.line(
                time_df,
                x='shipping date (DateOrders)',
                y='Orders Shipped',
                title="Orders Shipped Over Time",  # <- titre mis à jour
                markers=True
            )

            # Layout compact
            fig_time.update_layout(
                height=260,
                margin=dict(t=40, b=10, l=10, r=10),
                xaxis_title="Shipping Date",
                yaxis_title="Number of Orders Shipped",
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig_time, use_container_width=True)


render_log()