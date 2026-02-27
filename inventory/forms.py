"""
Django Forms for Inventory System
Handles: Category, Product, Sale, Stock Update, Date Filter
"""
from django import forms
from .models import Category, Product, Sale


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'cost_price', 'quantity', 'low_stock_threshold', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return qty


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold', 'sale_price', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select', 'id': 'id_product'}),
            'quantity_sold': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_sale_price'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity_sold = cleaned_data.get('quantity_sold')

        if product and quantity_sold:
            if quantity_sold <= 0:
                raise forms.ValidationError("Quantity sold must be at least 1.")
            if quantity_sold > product.quantity:
                raise forms.ValidationError(
                    f"Insufficient stock! Only {product.quantity} units available for '{product.name}'."
                )
        return cleaned_data


class StockUpdateForm(forms.Form):
    quantity_to_add = forms.IntegerField(
        label="Quantity to Add",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 2,
            'placeholder': 'Reason for stock update (optional)'
        })
    )


class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
