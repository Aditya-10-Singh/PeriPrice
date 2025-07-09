from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pickle
import numpy as np
import sqlite3
from datetime import datetime

app = FastAPI()

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

DB_FILE = "../perishables.db"

class Item(BaseModel):
    stock: int
    units_sold: int
    days_left: int
    day_of_week: int
    discount_flag: int

class UpdatePrice(BaseModel):
    product_id: int
    new_price: float

class SellItem(BaseModel):
    product_id: int
    quantity: int

@app.post("/predict_price")
def predict_price(item: Item):
    X_new = np.array([[item.stock, item.units_sold, item.days_left, item.day_of_week, item.discount_flag]])
    base_price = model.predict(X_new)[0]

    final_price = base_price
    if item.days_left <= 2:
        final_price *= 0.7  # 30% off if near expiry
    if item.stock >= 80:
        final_price *= 0.9  # 10% bulk discount

    return {"predicted_price": round(final_price, 2)}

@app.get("/get_inventory")
def get_inventory():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()
    return {"inventory": rows}

@app.post("/update_price")
def update_price(data: UpdatePrice):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE inventory SET price = ? WHERE product_id = ?", (data.new_price, data.product_id))
    conn.commit()
    conn.close()
    return {"status": "success", "updated_product_id": data.product_id}

@app.post("/predict_and_update")
def predict_and_update(item: Item):
    X_new = np.array([[item.stock, item.units_sold, item.days_left, item.day_of_week, item.discount_flag]])
    base_price = model.predict(X_new)[0]

    final_price = base_price
    if item.days_left <= 2:
        final_price *= 0.7
    if item.stock >= 80:
        final_price *= 0.9

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE inventory SET price = ? WHERE product_id = ?", (round(final_price, 2), 1))
    conn.commit()
    conn.close()

    return {"predicted_price": round(final_price, 2), "status": "price_updated"}

# POS simulation
@app.post("/sell_item")
def sell_item(sale: SellItem):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT stock, price FROM inventory WHERE product_id = ?", (sale.product_id,))
    row = c.fetchone()
    if row is None:
        conn.close()
        return JSONResponse(content={"error": "Product not found"}, status_code=404)

    current_stock, current_price = row

    if sale.quantity > current_stock:
        conn.close()
        return JSONResponse(content={"error": "Not enough stock"}, status_code=400)

    new_stock = current_stock - sale.quantity
    c.execute("UPDATE inventory SET stock = ? WHERE product_id = ?", (new_stock, sale.product_id))

    today = datetime.today().strftime("%Y-%m-%d")
    c.execute(
        "INSERT INTO sales (product_id, sale_date, units_sold, price_sold) VALUES (?, ?, ?, ?)",
        (sale.product_id, today, sale.quantity, current_price)
    )

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "product_id": sale.product_id,
        "quantity_sold": sale.quantity,
        "remaining_stock": new_stock
    }
