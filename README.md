# PeriPrice — Smart Dynamic Pricing & Inventory Management

**PeriPrice** is a full-stack dynamic pricing dashboard for perishable goods — built with **FastAPI**, **SQLite**, **Machine Learning**, and a **Streamlit** UI.
It helps businesses manage inventory, predict prices dynamically, record sales, and monitor trends — all in one place!

---

## 🚀 **Features**

✅ Predict smart prices for perishables based on:

* Stock level
* Units sold
* Days until expiry
* Day of week
* Discount rules

✅ Automatically adjust prices to reduce waste.

✅ Full **inventory dashboard**:

* Highlights expiring or low-stock items.
* Manual override to update prices.
* Record new sales directly.

✅ Secure **user login & registration** (multi-user support).

✅ Stores user credentials & sales records in **SQLite**.

✅ View daily sales trends with simple charts.

✅ Built-in **API testing** via Swagger UI.

---

## ⚙️ **Tech Stack**

* **Backend**: Python, FastAPI, SQLite, Pickle (for ML model)
* **Frontend**: Streamlit (minimal, clean, interactive)
* **ML Model**: Trained with scikit-learn (predicts base price)
* **API Docs**: Swagger UI (auto-generated)

---

## 📂 **Project Structure**

```
PeriPrice/
│
├── model/
│   └── model.pkl         # Trained ML model
│
├── data/
│   └── inventory_data.csv  # Initial stock data
│
├── app/
│   └── main.py           # FastAPI backend
│
├── dashboard/
│   └── app.py            # Streamlit frontend
│
├── perishables.db        # SQLite database (inventory, sales, users)
│
├── README.md
│
└── requirements.txt      # Python dependencies
```

---

## ⚡ **How to Run**

Follow these **step-by-step** instructions:

---

### 1️⃣ **Clone this repo**

```bash
git clone https://github.com/Aditya-10-Singh/PeriPrice.git
cd DynamicPricingProject
```

---

### 2️⃣ **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate    # For Mac/Linux
venv\Scripts\activate       # For Windows
```

---

### 3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

✅ Example `requirements.txt`:

```txt
fastapi
uvicorn
scikit-learn
pandas
numpy
streamlit
```

---

### 4️⃣ **Create and seed your database**

Run this once to create `perishables.db`:

```bash
python init_db.py
```

*(This script creates `inventory` and `sales` tables, and inserts sample data)*

---

### 5️⃣ **Run the FastAPI backend**

```bash
uvicorn app.main:app --reload
```

📌 **Test your API**
Visit 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You’ll see **Swagger UI** to test:

* `/predict_price`
* `/update_price`
* `/sell_item`

---

### 6️⃣ **Run the Streamlit dashboard**

```bash
streamlit run dashboard/app.py
```

This opens a **login page** → then your full dashboard.

---

## 🔑 **Authentication**

* **Register new users:** *(future enhancement)*
* **Current setup:** Hardcoded username/password in `app.py`.
* You can extend this to store users in a `users` table.

---

## ✨ **Possible Improvements**

✅ Add user registration flow (store hashed passwords).

✅ Add product management: Add/Delete products.

✅ Show predicted price inline on dashboard.

✅ Containerize with **Docker**.

✅ Host on **Heroku**, **Railway**, or **Render**.


---

## 📃 **License**

Open source — feel free to improve & share!

---

## ✅ **Support**

If you have any questions, open an issue or reach out!

---

**Happy Building!** 🚀✨
**#PeriPrice #DynamicPricing #FastAPI #Streamlit**

---


