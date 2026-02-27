"""
Sample Data Loader for Inventory & Stock Analysis System
=========================================================
Run this AFTER migrations and createsuperuser:

    python manage.py shell < load_data.py

This creates sample categories, products, and 200+ sales records
spread across the last 90 days so charts and analysis work immediately.
"""
import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from django.utils import timezone
from inventory.models import Category, Product, Sale

print("Clearing existing data...")
Sale.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()

# ── Categories ──────────────────────────────────────────────
cats = {}
for name in ['Electronics', 'Clothing', 'Food & Beverages', 'Stationery', 'Home Appliances']:
    cats[name] = Category.objects.create(name=name)
print(f"✓ {len(cats)} categories created")

# ── Products ─────────────────────────────────────────────────
# (name, category, sell_price, cost_price, qty, threshold)
products_data = [
    ('Laptop',           'Electronics',      65000, 50000,  25,  5),
    ('Smartphone',       'Electronics',      22000, 17000,  40,  8),
    ('Wireless Earbuds', 'Electronics',       3500,  2500,  60, 15),
    ('USB Cable',        'Electronics',        299,   150, 200, 30),
    ('Power Bank',       'Electronics',       2499,  1800,  35, 10),
    ('T-Shirt',          'Clothing',           499,   200, 150, 20),
    ('Jeans',            'Clothing',          1299,   600,  80, 15),
    ('Jacket',           'Clothing',          2499,  1200,  30,  5),
    ('Sports Shoes',     'Clothing',          3499,  2000,   8, 10),  # Low stock
    ('Coffee Beans',     'Food & Beverages',   799,   400, 100, 20),
    ('Green Tea',        'Food & Beverages',   299,   150, 120, 25),
    ('Protein Bar',      'Food & Beverages',   149,    80,   7, 15),  # Low stock
    ('Biscuit Pack',     'Food & Beverages',    89,    40, 300, 50),
    ('Notebook A4',      'Stationery',          99,    40, 500, 50),
    ('Ball Pen Pack',    'Stationery',           49,    20, 400, 50),
    ('Geometry Box',     'Stationery',          299,   150,   3, 10),  # Low stock
    ('Highlighters',     'Stationery',          199,    90,  80, 15),
    ('Mixer Grinder',    'Home Appliances',    3499,  2500,  15,  5),
    ('Table Fan',        'Home Appliances',    1899,  1200,  20,  5),
    ('LED Desk Lamp',    'Home Appliances',     899,   550,   6, 10),  # Low stock
]

product_objs = []
for name, cat, price, cost, qty, threshold in products_data:
    p = Product.objects.create(
        name=name,
        category=cats[cat],
        price=price,
        cost_price=cost,
        quantity=qty,
        low_stock_threshold=threshold,
    )
    product_objs.append(p)

print(f"✓ {len(product_objs)} products created")

# ── Sales Records (last 90 days) ─────────────────────────────
today = timezone.now()
sale_count = 0

# Give some products more sales to make fast-moving visible
weights = {
    'USB Cable': 15, 'Biscuit Pack': 12, 'Ball Pen Pack': 10,
    'Notebook A4': 10, 'Green Tea': 8, 'Wireless Earbuds': 7,
    'Smartphone': 5, 'T-Shirt': 5, 'Coffee Beans': 5,
    'Protein Bar': 4, 'Jeans': 3,
}

for product in product_objs:
    num_sales = weights.get(product.name, 2)
    for _ in range(num_sales * 8):  # multiply for enough records
        qty = random.randint(1, min(8, product.quantity + 20))
        days_ago = random.randint(0, 90)
        Sale.objects.create(
            product=product,
            quantity_sold=qty,
            sale_price=product.price,
            sale_date=today - timedelta(days=days_ago),
        )
        sale_count += 1

print(f"✓ {sale_count} sales records created (across last 90 days)")
print()
print("=" * 50)
print("  Sample data loaded successfully!")
print("  Run: python manage.py runserver")
print("  Visit: http://127.0.0.1:8000")
print("=" * 50)
