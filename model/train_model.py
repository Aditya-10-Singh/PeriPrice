import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

df = pd.read_csv("../inventory_data.csv")

X = df[['Stock', 'Units_Sold', 'Days_Left', 'Day_Of_Week', 'Discount_Flag']]
y = df['Price']

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Smarter model trained and saved as model.pkl")
