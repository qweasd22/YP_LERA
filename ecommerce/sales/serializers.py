from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

from rest_framework import serializers
from .models import Deal, Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'contact_person']

class DealSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

from rest_framework import serializers
from .models import Deal, DealItem

class DealItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealItem
        fields = ["product", "quantity"]

class DealSerializer(serializers.ModelSerializer):
    items = DealItemSerializer(many=True, read_only=True)
    
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    class Meta:
        model = Deal
        fields = ["id", "date", "is_wholesale", "discount", "total", "items", "customer_name"]


    
    
    
class DealCreateSerializer(serializers.ModelSerializer):
    items = DealItemSerializer(many=True)

    class Meta:
        model = Deal
        fields = ["customer", "is_wholesale", "discount", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        deal = Deal.objects.create(**validated_data)
        for item_data in items_data:
            DealItem.objects.create(deal=deal, **item_data)
        return deal
    
from .models import Deal

