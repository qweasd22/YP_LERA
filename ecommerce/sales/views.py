from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Deal

def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

def deal_create(request):
    if request.method == 'POST':
        # Логика обработки формы
        pass
    return render(request, 'sales/deal_create.html')

def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    return render(request, 'sales/deal_detail.html', {'deal': deal})

from rest_framework import generics
from .models import Deal
from .serializers import DealSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from .models import Deal
from .serializers import DealSerializer

from rest_framework import generics
from .models import Deal
from .serializers import DealSerializer

class DealListView(generics.ListAPIView):
    queryset = Deal.objects.all().prefetch_related("dealitem_set")
    serializer_class = DealSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

from rest_framework import generics
from .serializers import DealCreateSerializer

class DealCreateView(generics.CreateAPIView):
    queryset = Deal.objects.all()
    serializer_class = DealCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]