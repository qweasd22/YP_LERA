from django.contrib import admin
from .models import Product, Customer, Deal, DealItem

class DealItemInline(admin.TabularInline):
    model = DealItem
    extra = 1
    readonly_fields = ('line_total',)

    def line_total(self, obj):
        return obj.product.price * obj.quantity
    line_total.short_description = 'Сумма позиции'

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'customer', 'total_quantity', 'discount_percentage', 'subtotal', 'total')
    readonly_fields = ('date', 'total_quantity', 'discount_percentage', 'subtotal', 'total')
    inlines = [DealItemInline]
    fields = ('customer', 'date', 'total_quantity', 'discount_percentage', 'subtotal', 'total')
    
    @admin.display(description='Кол-во позиций')
    def total_quantity(self, obj):
        return obj.total_quantity

    @admin.display(description='Скидка %')
    def discount_percentage(self, obj):
        # obj.discount is Decimal fraction
        return f"{(obj.discount * 100):.0f}%"

    @admin.display(description='Сумма до скидки')
    def subtotal(self, obj):
        return f"{obj.subtotal:.2f} ₽"

    @admin.display(description='Итоговая сумма')
    def total(self, obj):
        return f"{obj.total:.2f} ₽"

# Регистрация других моделей
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone')
