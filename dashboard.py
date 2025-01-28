import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- Fungsi untuk membaca file dari URL ---
def load_data_from_url(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error: Tidak dapat membaca file dari URL: {url}. Detail: {e}")
        return None

# --- Input URL dari pengguna ---
st.sidebar.title("Upload Dataset melalui URL")
urls = {
    "df_items": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/order_reviews_dataset.csv"),
    "df_reviews": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/order_reviews_dataset.csv"),
    "df_orders": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/orders_dataset.csv"),
    "df_products": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/products_dataset.csv"),
    "df_sellers": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/sellers_dataset.csv"),
    "df_payments": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/order_payments_dataset.csv"),
    "df_customers": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/customers_dataset.csv"),
    "df_category": st.sidebar.text_input("https://github.com/leviathan712/submission-raasyah/blob/main/product_category_name_translation.csv"),
}

# --- Membaca dataset ---
try:
    df_items = load_data_from_url(urls["df_items"])
    df_reviews = load_data_from_url(urls["df_reviews"])
    df_orders = load_data_from_url(urls["df_orders"])
    df_products = load_data_from_url(urls["df_products"])
    df_sellers = load_data_from_url(urls["df_sellers"])
    df_payments = load_data_from_url(urls["df_payments"])
    df_customers = load_data_from_url(urls["df_customers"])
    df_category = load_data_from_url(urls["df_category"])
    
    if None in [df_items, df_reviews, df_orders, df_products, df_sellers, df_payments, df_customers, df_category]:
        st.stop()
    
    df = df_orders.merge(df_items, on='order_id', how='inner')
    df = df.merge(df_payments, on='order_id', how='inner', validate='m:m')
    df = df.merge(df_reviews, on='order_id', how='inner')
    df = df.merge(df_products, on='product_id', how='inner')
    df = df.merge(df_customers, on='customer_id', how='inner')
    df = df.merge(df_sellers, on='seller_id', how='inner')
except Exception as e:
    st.error(f"Error: Terjadi masalah saat memproses dataset. Detail: {e}")
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
    df['review_score'].hist(bins=5, color='skyblue', edgecolor='black', ax=ax)
    ax.set(title='Review Skor Distribusi', xlabel='Skor Review', ylabel='Frekuensi')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# --- Trend Penjualanan Bulanan ---
elif page == "Trend Penjualanan Bulanan":
    st.subheader("Trend Penjualanan Bulanan")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    monthly_sales = df.groupby(df['order_purchase_timestamp'].dt.to_period('M'))['price'].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales.index.astype(str), monthly_sales, marker='o', linestyle='-', color='skyblue', linewidth=2)
    ax.set(title='Trend Penjualanan Bulanan', xlabel='Bulan', ylabel='Total Penjualan')
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# --- 10 Kategori Produk Terbaik ---
elif page == "10 Kategori Produk Terbaik":
    st.subheader("10 Kategori Produk Terbaik")
    top_categories = df['product_category_name'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    top_categories.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
    ax.set(title='10 Kategori Produk Terbaik', xlabel='Kategori Produk', ylabel='Jumlah Pemesanan')
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
