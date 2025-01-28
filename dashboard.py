import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

try:
    df_items = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/order_items_dataset.csv")
    df_reviews = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/order_reviews_dataset.csv")
    df_orders = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/orders_dataset.csv")
    df_products = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/products_dataset.csv")
    df_sellers = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/sellers_dataset.csv")
    df_payments = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/order_payments_dataset.csv")
    df_customers = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/customers_dataset.csv")
    df_category = pd.read_csv("https://raw.githubusercontent.com/leviathan712/submission-raasyah/main/product_category_name_translation.csv")
    df = df_orders.merge(df_items, on='order_id', how='inner')
    df = df.merge(df_payments, on='order_id', how='inner', validate='m:m')
    df = df.merge(df_reviews, on='order_id', how='inner')
    df = df.merge(df_products, on='product_id', how='inner')
    df = df.merge(df_customers, on='customer_id', how='inner')
    df = df.merge(df_sellers, on='seller_id', how='inner')
    df_data = df
except FileNotFoundError:
    st.error("Error: not found. Please upload the file.")
    st.stop()

# --- Page Title ---
st.title("E-commerce Sales Analysis Dashboard")

# --- Sidebar Menu ---
page = st.sidebar.selectbox("Pilih Visual Data", [
    "Review Skor Distribusi", 
    "Trend Penjualanan Bulanan", 
    "10 Kategori Produk Terbaik",
])

# --- Review Skor Distribusi ---
if page == "Review Skor Distribusi":
    st.subheader("Review Skor Distribusi")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_data['review_score'].hist(bins=5, color='skyblue', edgecolor='black', ax=ax)
    ax.set(title='Review Skor Distribusi', xlabel='Skor Review', ylabel='Frekuensi')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# --- Trend Penjualanan Bulanan ---
elif page == "Trend Penjualanan Bulanan":
    st.subheader("Trend Penjualanan Bulanan")
    df_data['order_purchase_timestamp'] = pd.to_datetime(df_data['order_purchase_timestamp'])
    monthly_sales = df_data.groupby(df_data['order_purchase_timestamp'].dt.to_period('M'))['price'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales.index.astype(str), monthly_sales, marker='o', linestyle='-', color='skyblue', linewidth=2)
    ax.set(title='Trend Penjualanan Bulanan', xlabel='Bulan', ylabel='Total Penjualan')
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# --- 10 Kategori Produk Terbaik ---
elif page == "10 Kategori Produk Terbaik":
    st.subheader("10 Kategori Produk Terbaik")
    top_categories = df_data['product_category_name'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    top_categories.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set(title='10 Kategori Produk Terbaik', xlabel='Kategori Produk', ylabel='Jumlah Pemesanan')
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
