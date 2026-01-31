import pandas as pd
from pathlib import Path

def type_data(df):
    # Conversion des dates
    df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"], errors="coerce")
    df["shipping date (DateOrders)"] = pd.to_datetime(df["shipping date (DateOrders)"], errors="coerce")
    
    # Colonnes catégorielles
    cat_cols = [
        "Type", "Delivery Status", "Order Status", "Shipping Mode",
        "Customer Segment", "Category Name", "Department Name",
        "Market", "Order Region", "Order State"
    ]
    for col in cat_cols:
        df[col] = df[col].astype("category")
    
    # Colonnes string
    str_cols = [
        "Customer Email", "Customer Password", "Customer Fname",
        "Customer Lname", "Customer City", "Customer State",
        "Customer Country", "Customer Street", "Customer Zipcode",
        "Order Zipcode", "Product Name", "Product Image"
    ]
    for col in str_cols:
        df[col] = df[col].astype(str)
    
    # Colonnes numériques restantes
    num_cols = [
        "Days for shipping (real)", "Days for shipment (scheduled)",
        "Late_delivery_risk", "Customer Id", "Order Customer Id",
        "Order Id", "Order Item Id", "Order Item Cardprod Id",
        "Order Item Product Price", "Order Item Quantity",
        "Order Item Discount", "Order Item Discount Rate",
        "Order Item Total", "Order Profit Per Order", "Order Item Profit Ratio",
        "Sales", "Benefit per order", "Sales per customer",
        "Product Card Id", "Product Category Id", "Product Price", "Product Status",
        "Latitude", "Longitude", "Department Id", "Category Id"
    ]
    for col in num_cols:
        df[col] = df[col].astype(float)  # int ou float selon besoin
    
    return df
