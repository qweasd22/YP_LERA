from django.contrib import admin
from .models import Product, Customer, Deal, DealItem

class DealItemInline(admin.TabularInline):
    model = DealItem
    extra = 1

class DealAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'created_at')

admin.site.register(Product)
admin.site.register(Customer)
from rest_framework.authtoken.models import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)


