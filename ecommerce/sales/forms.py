# sales/forms.py
from django import forms
from .models import Deal, DealItem, Customer, Product

from django import forms
from django.forms import modelformset_factory
from .models import Deal, Product
from django.forms.models import inlineformset_factory


class DealForm(forms.ModelForm):
    class Meta:
        model  = Deal
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
        }

class DealItemForm(forms.ModelForm):
    class Meta:
        model  = DealItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 1}),
        }

DealItemFormSet = inlineformset_factory(
    Deal, DealItem,
    form=DealItemForm,
    extra=1, can_delete=True
)
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'contact_person'] 
        
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите наименование'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену'}),
        }