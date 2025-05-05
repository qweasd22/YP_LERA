# sales/models.py
from django.db import models
from decimal import Decimal

from decimal import Decimal

class Product(models.Model):
    name  = models.CharField("Наименование", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name           = models.CharField("Покупатель", max_length=255)
    address        = models.TextField("Адрес", blank=True)
    phone          = models.CharField("Телефон", max_length=20, blank=True)
    contact_person = models.CharField("Контактное лицо", max_length=255, blank=True)

    def __str__(self):
        return self.name

class Deal(models.Model):
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент")
    date        = models.DateField("Дата", auto_now_add=True)

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def discount(self):
        qty = self.total_quantity
        if qty >= 1000: return Decimal('0.20')
        if qty >= 100:  return Decimal('0.10')
        if qty >= 10:   return Decimal('0.05')
        return Decimal('0')

    @property
    def subtotal(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    @property
    def total(self):
        return self.subtotal * (1 - self.discount)

    def __str__(self):
        return f"Сделка #{self.id} — {self.customer.name}"

class DealItem(models.Model):
    deal     = models.ForeignKey(Deal, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
