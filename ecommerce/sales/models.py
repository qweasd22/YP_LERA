from django.db import models

class Product(models.Model):
    name = models.CharField("Наименование", max_length=255)
    wholesale_price = models.DecimalField("Оптовая цена", max_digits=10, decimal_places=2)
    retail_price = models.DecimalField("Розничная цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField("Наименование", max_length=255)
    address = models.TextField("Адрес")
    phone = models.CharField("Телефон", max_length=20)
    contact_person = models.CharField("Контактное лицо", max_length=255)

    def __str__(self):
        return self.name

class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField("Дата сделки", auto_now_add=True)
    is_wholesale = models.BooleanField("Оптовая продажа", default=False)
    discount = models.DecimalField("Скидка %", max_digits=5, decimal_places=2, default=0)
    
    @property
    def total(self):
        total = sum(item.subtotal for item in self.dealitem_set.all())
        return total * (1 - self.discount/100)

class DealItem(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)
    
    @property
    def subtotal(self):
        price = self.product.wholesale_price if self.deal.is_wholesale else self.product.retail_price
        return price * self.quantity