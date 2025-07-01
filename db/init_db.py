import sqlite3
import pandas as pd

# ✅ Load your CSV
df = pd.read_csv("inventory_data.csv")

# ✅ Connect to your DB — adjust path as needed!
conn = sqlite3.connect("../perishables.db")
c = conn.cursor()

# ✅ -------------------------
# Drop old tables if they exist
# -------------------------
c.execute("DROP TABLE IF EXISTS inventory")
c.execute("DROP TABLE IF EXISTS sales")

# ✅ -------------------------
# Create fresh inventory table
# -------------------------
c.execute('''
    CREATE TABLE inventory (
        product_id INTEGER,
        product_name TEXT,
        stock INTEGER,
        units_sold INTEGER,
        price REAL,
        days_left INTEGER,
        expiry_date TEXT
    )
''')

# ✅ -------------------------
# Insert CSV rows into inventory
# -------------------------
for _, row in df.iterrows():
    c.execute('''
        INSERT INTO inventory (product_id, product_name, stock, units_sold, price, days_left, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['Product_ID'],
        row['Product_Name'],
        row['Stock'],
        row['Units_Sold'],
        row['Price'],
        row['Days_Left'],
        row['Expiry_Date']
    ))

# ✅ -------------------------
# Create sales table — new!
# -------------------------
c.execute('''
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        sale_date TEXT,
        units_sold INTEGER,
        price_sold REAL
    )
''')

# ✅ -------------------------
# Commit & close connection
# -------------------------
conn.commit()
conn.close()

print("✅ perishables.db recreated with inventory + sales tables.")
