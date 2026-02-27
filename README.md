# 📦 Inventory & Stock Analysis System

A full-stack web-based inventory management system built with **Django**, **Pandas**, and **Chart.js**.

---

## 🚀 Features

- ✅ Add / Edit / Delete Products & Categories
- ✅ Record Sales — auto-reduces stock on sale
- ✅ Low Stock Alerts (per-product threshold)
- ✅ Fast-Moving Product Detection (Pandas, last 30 days)
- ✅ Monthly Sales Report (Pandas resample)
- ✅ Interactive Charts (Chart.js — Line, Bar, Pie)
- ✅ Stock Valuation (total inventory worth)
- ✅ Sales History with Date Filter
- ✅ Secure Login/Logout System

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Backend    | Django 4.2        |
| Database   | SQLite (local)    |
| Analysis   | Pandas 2.x        |
| Frontend   | Bootstrap 5 + JS  |
| Charts     | Chart.js 4.x      |

---

## ⚙️ Setup Instructions

### Step 1 — Prerequisites
- Python 3.10 or higher
- pip

### Step 2 — Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Create Admin User
```bash
python manage.py createsuperuser
# Enter username, email (optional), password
```

### Step 6 — Load Sample Data (Optional but Recommended)
```bash
python load_data.py
```
This adds 20 products across 5 categories and 1000+ sale records
so the dashboard charts and analysis are populated immediately.

### Step 7 — Run the Server
```bash
python manage.py runserver
```

### Step 8 — Open in Browser
```
http://127.0.0.1:8000
```
Log in with the credentials you created in Step 5.

---

## 📁 Project Structure

```
inventory_project/
│
├── manage.py
├── requirements.txt
├── load_data.py               ← Sample data loader
├── db.sqlite3                 ← Auto-created after migrate
│
├── inventory_project/         ← Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── inventory/                 ← Main app
│   ├── models.py              ← Category, Product, Sale
│   ├── views.py               ← All request handlers
│   ├── urls.py                ← URL routes
│   ├── forms.py               ← Form classes
│   ├── analysis.py            ← Pandas analysis engine
│   └── admin.py
│
├── templates/                 ← HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── products/
│   └── sales/
│       reports/
│
└── static/
    ├── css/style.css
    └── js/charts.js
```

---

## 🔗 URL Routes

| URL | Page |
|-----|------|
| `/` | Dashboard |
| `/products/` | Product list |
| `/products/add/` | Add product |
| `/categories/` | Category list |
| `/sales/record/` | Record a sale |
| `/sales/history/` | Sales history |
| `/reports/analysis/` | Analysis report |
| `/admin/` | Django admin panel |

---

## 📊 How Analysis Works

**Fast-Moving Products:**
```
Filter sales where date >= today - 30 days
→ Group by product name
→ Sum quantity_sold per product
→ Sort descending
→ Take top 5
```

**Monthly Report:**
```
Set sale_date as DataFrame index
→ resample('ME')  # group by month-end
→ Aggregate: sum revenue, sum units, count transactions
→ Format month as 'Jan 2024'
```

**Low Stock Detection:**
```
For each product:
  if quantity <= low_stock_threshold → flag as LOW
  deficit = threshold - quantity
Sort by deficit descending (most critical first)
```

---

## 👤 Author

[Your Name] | [Your College] | BCA/B.Tech | [Year]

---

## 📝 License

Open source — for educational purposes only.
