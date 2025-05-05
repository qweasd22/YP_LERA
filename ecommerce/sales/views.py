from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, Customer, Deal, DealItem
from .forms import DealForm, DealItemFormSet
from django.shortcuts import redirect

def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

def deal_list(request):
    deals = Deal.objects.prefetch_related('items__product')
    return render(request, 'sales/deal_list.html', {'deals': deals})

def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    return render(request, 'sales/deal_detail.html', {'deal': deal})

def deal_create(request):
    prefix = 'items'
    if request.method == 'POST':
        form    = DealForm(request.POST)
        formset = DealItemFormSet(request.POST, prefix=prefix)
        if form.is_valid() and formset.is_valid():
            deal = form.save()
            formset.instance = deal
            formset.save()
            return redirect('sales:deal_detail', pk=deal.pk)
    else:
        form    = DealForm()
        formset = DealItemFormSet(prefix=prefix)
    return render(request, 'sales/deal_form.html', {
        'form': form,
        'formset': formset,
        'prefix': prefix,
    })

def index(request):
    """Главная страница"""
    return render(request, 'sales/index.html')


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
from .forms import CustomerForm
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/add_customer.html', {'form': form})