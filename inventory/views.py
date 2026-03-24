"""
Views for Inventory & Stock Analysis System
Handles all HTTP requests and business logic
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse

from .models import Category, Product, Sale
from .forms import CategoryForm, ProductForm, SaleForm, StockUpdateForm, DateFilterForm
from . import analysis


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):
    """Main dashboard with KPIs and chart data"""
    stats = analysis.get_dashboard_stats()
    fast_moving = analysis.get_fast_moving_products(days=30, top_n=5)
    low_stock = analysis.get_low_stock_products()
    recent_sales = Sale.objects.select_related('product').order_by('-sale_date')[:10]

    return render(request, 'dashboard.html', {
        'stats': stats,
        'fast_moving': fast_moving,
        'low_stock': low_stock[:5],
        'recent_sales': recent_sales,
        'page_title': 'Dashboard',
    })


# ============================================================
# CATEGORY VIEWS
# ============================================================

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {
        'categories': categories,
        'page_title': 'Categories'
    })


@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form, 'page_title': 'Add Category'})


# ============================================================
# PRODUCT VIEWS
# ============================================================

@login_required
def product_list(request):
    products = Product.objects.select_related('category').all()

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__id=category_filter)

    low_stock_filter = request.GET.get('low_stock')
    if low_stock_filter:
        products = [p for p in products if p.is_low_stock]

    categories = Category.objects.all()

    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
        'page_title': 'Products',
    })


@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add.html', {'form': form, 'page_title': 'Add Product'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{product.name}' updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit.html', {
        'form': form, 'product': product, 'page_title': 'Edit Product'
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"'{name}' deleted successfully.")
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {
        'product': product, 'page_title': 'Delete Product'
    })


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sales = Sale.objects.filter(product=product).order_by('-sale_date')
    return render(request, 'products/detail.html', {
        'product': product,
        'sales': sales,
        'page_title': product.name
    })


@login_required
def stock_update(request, pk):
    """Add stock to a product (restock operation)"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity_to_add']
            product.quantity += qty
            product.save()
            messages.success(
                request,
                f"Stock updated! Added {qty} units to '{product.name}'. New stock: {product.quantity}"
            )
            return redirect('product_list')
    else:
        form = StockUpdateForm()
    return render(request, 'products/stock_update.html', {
        'form': form, 'product': product, 'page_title': 'Update Stock'
    })


# ============================================================
# SALES VIEWS
# ============================================================

@login_required
def record_sale(request):
    """
    Record a new sale.
    Uses atomic transaction to ensure sale record + stock reduction
    both succeed or both fail together.
    """
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            qty_sold = form.cleaned_data['quantity_sold']

            try:
                with transaction.atomic():
                    form.save()
                    product.quantity -= qty_sold
                    product.save()

                    messages.success(
                        request,
                        f"Sale recorded! {qty_sold} units of '{product.name}'. "
                        f"Remaining stock: {product.quantity}"
                    )

                    if product.is_low_stock:
                        messages.warning(
                            request,
                            f"⚠️ LOW STOCK ALERT: '{product.name}' has only {product.quantity} units left!"
                        )

                return redirect('sale_history')

            except Exception as e:
                messages.error(request, f"Error recording sale: {str(e)}")
    else:
        form = SaleForm()

    return render(request, 'sales/record.html', {'form': form, 'page_title': 'Record Sale'})


@login_required
def sale_history(request):
    """View all sales with optional date range filter"""
    sales = Sale.objects.select_related('product__category').order_by('-sale_date')
    form = DateFilterForm(request.GET or None)

    if form.is_valid():
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')
        if start:
            sales = sales.filter(sale_date__date__gte=start)
        if end:
            sales = sales.filter(sale_date__date__lte=end)

    total_revenue = sum(s.total_revenue for s in sales)

    return render(request, 'sales/history.html', {
        'sales': sales,
        'form': form,
        'total_revenue': total_revenue,
        'page_title': 'Sales History',
    })


# ============================================================
# ANALYSIS & REPORTS
# ============================================================

@login_required
def analysis_report(request):
    """Full analysis page with all Pandas-generated data"""
    return render(request, 'reports/analysis.html', {
        'fast_moving': analysis.get_fast_moving_products(days=30, top_n=5),
        'monthly_report': analysis.get_monthly_sales_report(),
        'category_breakdown': analysis.get_category_sales_breakdown(),
        'low_stock': analysis.get_low_stock_products(),
        'stats': analysis.get_dashboard_stats(),
        'page_title': 'Stock Analysis Report',
    })


# ============================================================
# API ENDPOINTS (JSON for Chart.js)
# ============================================================

@login_required
def api_chart_data(request):
    """Returns JSON data for all dashboard charts"""
    monthly = analysis.get_monthly_sales_report()
    category_data = analysis.get_category_sales_breakdown()
    product_data = analysis.get_product_sales_chart_data()

    return JsonResponse({
        'monthly': {
            'labels': [m['month'] for m in monthly],
            'revenues': [float(m['total_revenue']) for m in monthly],
            'units': [int(m['units_sold']) for m in monthly],
        },
        'categories': {
            'labels': [c['category'] for c in category_data],
            'revenues': [float(c['revenue']) for c in category_data],
        },
        'products': {
            'labels': [p['product'] for p in product_data],
            'revenues': [float(p['revenue']) for p in product_data],
        },
    })


@login_required
def api_product_price(request):
    """Returns price and stock of a product — used for auto-fill in sale form"""
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({
            'price': float(product.price),
            'stock': product.quantity,
            'name': product.name
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
