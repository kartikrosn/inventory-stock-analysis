"""
Database models for Inventory & Stock Analysis System
Defines: Category, Product, Sale
"""
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Product category (e.g., Electronics, Clothing, Food)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model — stores item details and current stock"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        """Returns True if stock is at or below threshold"""
        return self.quantity <= self.low_stock_threshold

    @property
    def stock_value(self):
        """Returns total value of current stock"""
        return self.price * self.quantity

    @property
    def total_sold(self):
        """Returns total units sold for this product"""
        return sum(sale.quantity_sold for sale in self.sales.all())


class Sale(models.Model):
    """
    Sales record — each entry represents one sale transaction.
    Stock is automatically reduced via the view when a sale is recorded.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sales'
    )
    quantity_sold = models.IntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold} units on {self.sale_date.strftime('%d-%m-%Y')}"

    @property
    def total_revenue(self):
        """Revenue from this single sale"""
        return self.sale_price * self.quantity_sold
