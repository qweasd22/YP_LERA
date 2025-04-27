# sales/forms.py
from django import forms
from .models import Deal, DealItem, Customer, Product

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['customer', 'is_wholesale', 'discount']

    # Динамические поля для товаров
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all()