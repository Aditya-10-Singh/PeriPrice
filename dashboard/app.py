import os
import sqlite3
import pandas as pd
import streamlit as st
import requests
import hashlib

# --- CONFIG ---
DB_FILE = "../perishables.db"
FASTAPI_URL = "http://127.0.0.1:8000"

# --- PAGE CONFIG ---
st.set_page_config(page_title="PeriPrice", page_icon="📊", layout="wide")

# --- STYLES ---
st.markdown("""
    <style>
    body { background-color: #f8f9fc; }
    .main { background-color: #ffffff; border-radius: 10px; padding: 2rem; }
    h1, h2, h3 { color: #333333; }
    .stButton>button { background-color: #ff5e78; color: white; border: None; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- HELPERS ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

create_users_table()

# --- SESSION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- AUTH ---
if not st.session_state.logged_in:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## ✨ PeriPrice")
        st.markdown("Your gateway to better pricing and inventory decisions.")
    with col2:
        option = st.selectbox("Select", ["Login", "Register"])

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if option == "Register":
            if st.button("Register"):
                hashed_pw = hash_password(password)
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
                    conn.commit()
                    st.success("✅ Registered! You can login now.")
                except:
                    st.error("⚠ Username already exists.")
                conn.close()
        else:
            if st.button("Login"):
                hashed_pw = hash_password(password)
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
                result = c.fetchone()
                conn.close()
                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
    st.stop()

# --- DASHBOARD ---
st.title(f"📊 PeriPrice Dashboard — Hello, {st.session_state.username}!")

# --- LOAD DATA ---
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM inventory", conn)
try:
    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
except:
    sales_df = pd.DataFrame()
conn.close()

# --- Expiry Alert ---
expiring = df[df['days_left'] <= 2]
if not expiring.empty:
    st.warning(f"⚠ {len(expiring)} items expiring soon!")
    st.dataframe(expiring)

# --- Inventory Table ---
st.subheader("📦 Full Inventory")
def highlight(row):
    if row['days_left'] <= 2:
        return ['background-color: yellow']*len(row)
    elif row['stock'] <= 10:
        return ['background-color: red']*len(row)
    else:
        return ['']*len(row)
st.dataframe(df.style.apply(highlight, axis=1))

# --- Predict Price ---
st.subheader("💰 Predict Price")
with st.form("predict_form"):
    pid = st.number_input("Product ID", min_value=1, step=1)
    stock = st.number_input("Stock", min_value=0)
    units_sold = st.number_input("Units Sold", min_value=0)
    days_left = st.number_input("Days Left", min_value=0)
    day_of_week = st.selectbox("Day of Week (0=Mon ... 6=Sun)", list(range(7)))
    discount_flag = st.selectbox("Discount Flag (0=No, 1=Yes)", [0, 1])
    submitted = st.form_submit_button("Predict")
    if submitted:
        payload = {
            "stock": stock,
            "units_sold": units_sold,
            "days_left": days_left,
            "day_of_week": day_of_week,
            "discount_flag": discount_flag
        }
        res = requests.post(f"{FASTAPI_URL}/predict_price", json=payload)
        if res.status_code == 200:
            pred = res.json()['predicted_price']
            st.success(f"💲 Predicted Price: ${pred}")
        else:
            st.error("❌ Prediction failed.")

# --- Manual Price Update ---
st.subheader("✏ Manual Price Update")
pid = st.number_input("Product ID to Update", min_value=1, step=1, key="pid_update")
new_price = st.number_input("New Price", min_value=0.0, format="%.2f")
if st.button("Update Price"):
    res = requests.post(f"{FASTAPI_URL}/update_price",
                        json={"product_id": pid, "new_price": new_price})
    if res.status_code == 200:
        st.success(f"✅ Updated price for Product {pid}")
        st.rerun()
    else:
        st.error("❌ Update failed.")

# --- Simulate Sale ---
st.subheader("🛒 Make a Sale")
sid = st.number_input("Product ID to Sell", min_value=1, step=1)
qty = st.number_input("Quantity Sold", min_value=1, step=1)
if st.button("Record Sale"):
    res = requests.post(f"{FASTAPI_URL}/sell_item",
                        json={"product_id": sid, "quantity": qty})
    if res.status_code == 200:
        out = res.json()
        st.success(f"✅ Sold {qty} units. Remaining: {out['remaining_stock']}")
        st.rerun()
    else:
        st.error("❌ Sale failed. Check stock!")

# --- Sales Trend ---
st.subheader("📈 Sales Trend")
if not sales_df.empty:
    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
    daily = sales_df.groupby('sale_date')['units_sold'].sum().reset_index()
    daily = daily.rename(columns={"sale_date": "Date", "units_sold": "Units Sold"})
    st.line_chart(daily)
else:
    st.info("ℹ No sales data yet.")

# --- Logout ---
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()