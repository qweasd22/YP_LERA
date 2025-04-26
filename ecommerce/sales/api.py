from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Customer, Deal, DealItem
from .serializers import *

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['name', 'phone']

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()  # Добавляем явное указание queryset
    serializer_class = DealSerializer
    
    

class DealItemViewSet(viewsets.ModelViewSet):
    queryset = DealItem.objects.all()
    serializer_class = DealItemSerializer