"""
URL routing for inventory app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/stock/', views.stock_update, name='stock_update'),

    # Sales
    path('sales/record/', views.record_sale, name='record_sale'),
    path('sales/history/', views.sale_history, name='sale_history'),

    # Reports
    path('reports/analysis/', views.analysis_report, name='analysis_report'),

    # API endpoints
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
    path('api/product-price/', views.api_product_price, name='api_product_price'),
]
