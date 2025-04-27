from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Deal, DealItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

from django.shortcuts import render, redirect
from .forms import DealForm


def create_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save(commit=False)
            deal.save()

            # Обработка товаров
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            DealItem.objects.create(deal=deal, product=product, quantity=quantity)

            return redirect('deal_list')
    else:
        form = DealForm()
    return render(request, 'sales/deal_create.html', {'form': form})

def index(request):
    """Главная страница"""
    return render(request, 'sales/index.html')
def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'sales/deal_list.html', {'deals': deals})
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
    serializer_class = DealSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]