"""
Data Analysis Module — uses Pandas for stock & sales analysis
FIXED: Timezone-aware datetime comparison bug resolved.
"""
import pandas as pd
from django.utils import timezone
from datetime import timedelta
from .models import Sale, Product


def get_sales_dataframe():
    """
    Convert all Sales records to a Pandas DataFrame.
    """
    sales = Sale.objects.select_related('product__category').all()

    if not sales.exists():
        return pd.DataFrame()

    data = []
    for sale in sales:
        data.append({
            'sale_id': sale.id,
            'product': sale.product.name,
            'category': sale.product.category.name if sale.product.category else 'Uncategorized',
            'quantity_sold': sale.quantity_sold,
            'sale_price': float(sale.sale_price),
            'revenue': float(sale.total_revenue),
            'sale_date': sale.sale_date,
        })

    df = pd.DataFrame(data)
    # Convert to UTC-aware datetime — critical for timezone-safe comparisons
    df['sale_date'] = pd.to_datetime(df['sale_date'], utc=True)
    return df


def get_fast_moving_products(days=30, top_n=5):
    """
    Fast-moving = products with highest total quantity sold in last N days.
    """
    cutoff_date = timezone.now() - timedelta(days=days)

    sales = Sale.objects.filter(
        sale_date__gte=cutoff_date
    ).select_related('product')

    if not sales.exists():
        return []

    data = [{'product': s.product.name, 'quantity_sold': s.quantity_sold} for s in sales]
    df = pd.DataFrame(data)

    fast_moving = (
        df.groupby('product')['quantity_sold']
        .sum()
        .reset_index()
        .sort_values('quantity_sold', ascending=False)
        .head(top_n)
    )

    return fast_moving.to_dict('records')


def get_monthly_sales_report():
    """
    Aggregate sales by calendar month using Pandas resample.
    """
    df = get_sales_dataframe()

    if df.empty:
        return []

    df_indexed = df.set_index('sale_date').copy()

    monthly = df_indexed.resample('M').agg(
        total_revenue=('revenue', 'sum'),
        units_sold=('quantity_sold', 'sum'),
        transactions=('sale_id', 'count')
    ).reset_index()

    monthly['month'] = monthly['sale_date'].dt.strftime('%b %Y')

    return monthly[['month', 'total_revenue', 'units_sold', 'transactions']].to_dict('records')


def get_category_sales_breakdown():
    """
    Revenue broken down by product category.
    """
    df = get_sales_dataframe()

    if df.empty:
        return []

    breakdown = (
        df.groupby('category')
        .agg(revenue=('revenue', 'sum'), units=('quantity_sold', 'sum'))
        .reset_index()
        .sort_values('revenue', ascending=False)
    )

    return breakdown.to_dict('records')


def get_low_stock_products():
    """
    Returns all products where quantity <= low_stock_threshold.
    Sorted by deficit (most critical first).
    """
    products = Product.objects.all()
    low_stock = []

    for p in products:
        if p.is_low_stock:
            low_stock.append({
                'id': p.id,
                'name': p.name,
                'quantity': p.quantity,
                'threshold': p.low_stock_threshold,
                'deficit': p.low_stock_threshold - p.quantity,
            })

    return sorted(low_stock, key=lambda x: x['deficit'], reverse=True)


def get_dashboard_stats():
    """
    Summary statistics for the dashboard.
    FIXED: Use tz_localize instead of passing tz= to pd.Timestamp constructor.
    """
    df = get_sales_dataframe()
    products = Product.objects.all()

    total_stock_value = sum(float(p.stock_value) for p in products)

    if not df.empty:
        # FIX: Correct way to create timezone-aware Timestamp for comparison
        cutoff_naive = timezone.now() - timedelta(days=30)
        cutoff = pd.Timestamp(cutoff_naive).tz_convert('UTC')

        recent = df[df['sale_date'] >= cutoff]
        monthly_revenue = float(recent['revenue'].sum()) if not recent.empty else 0
        total_units_sold = int(df['quantity_sold'].sum())
        total_revenue = float(df['revenue'].sum())
    else:
        monthly_revenue = 0
        total_units_sold = 0
        total_revenue = 0

    return {
        'total_products': products.count(),
        'low_stock_count': sum(1 for p in products if p.is_low_stock),
        'total_stock_value': round(total_stock_value, 2),
        'monthly_revenue': round(monthly_revenue, 2),
        'total_revenue': round(total_revenue, 2),
        'total_units_sold': total_units_sold,
    }


def get_product_sales_chart_data():
    """Returns top 10 products by revenue for bar chart."""
    df = get_sales_dataframe()
    if df.empty:
        return []

    top_products = (
        df.groupby('product')['revenue']
        .sum()
        .reset_index()
        .sort_values('revenue', ascending=False)
        .head(10)
    )
    return top_products.to_dict('records')
