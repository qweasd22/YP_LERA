from django.contrib import admin
from .models import Product, Customer, Deal, DealItem

class DealItemInline(admin.TabularInline):
    model = DealItem
    extra = 1

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    inlines = [DealItemInline]
    list_display = ('date', 'customer', 'total')

admin.site.register(Product)
admin.site.register(Customer)
from rest_framework.authtoken.models import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)