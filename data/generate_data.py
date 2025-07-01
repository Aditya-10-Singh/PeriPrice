import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

products = [
    {"Product_ID": 1, "Product_Name": "Milk", "Shelf_Life": 7, "Base_Price": 50},
    {"Product_ID": 2, "Product_Name": "Yogurt", "Shelf_Life": 10, "Base_Price": 30},
]

records = []
num_days = 30
start_date = datetime.today()

for product in products:
    stock = random.randint(50, 100)
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        expiry = start_date + timedelta(days=product['Shelf_Life'])
        days_left = (expiry - date).days
        price = product['Base_Price']
        
        if days_left <= 2:
            price *= 0.7
            discount_flag = 1
        elif days_left <= 4:
            price *= 0.85
            discount_flag = 1
        else:
            discount_flag = 0
        
        units_sold = random.randint(5, 15)
        day_of_week = date.weekday()  # Monday=0, Sunday=6

        records.append({
            "Product_ID": product["Product_ID"],
            "Product_Name": product["Product_Name"],
            "Date": date.date(),
            "Stock": stock,
            "Units_Sold": units_sold,
            "Price": round(price, 2),
            "Days_Left": days_left,
            "Expiry_Date": expiry.date(),
            "Day_Of_Week": day_of_week,
            "Discount_Flag": discount_flag
        })
        stock -= units_sold

df = pd.DataFrame(records)
df.to_csv("inventory_data.csv", index=False)
print("Dataset saved as inventory_data.csv")
