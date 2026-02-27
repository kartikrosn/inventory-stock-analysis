"""
Django Admin configuration
"""
from django.contrib import admin
from .models import Category, Product, Sale


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'low_stock_threshold', 'is_low_stock_display', 'created_at']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['quantity', 'low_stock_threshold']

    def is_low_stock_display(self, obj):
        return obj.is_low_stock
    is_low_stock_display.boolean = True
    is_low_stock_display.short_description = 'Low Stock?'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity_sold', 'sale_price', 'revenue_display', 'sale_date']
    list_filter = ['sale_date', 'product__category']
    search_fields = ['product__name']
    date_hierarchy = 'sale_date'

    def revenue_display(self, obj):
        return f"₹{obj.total_revenue}"
    revenue_display.short_description = 'Revenue'
