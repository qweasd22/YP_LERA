from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('deals/<int:pk>/', views.deal_detail, name='deal_detail'),
    path('deals/', views.deal_list,   name='deal_list'),
    path('deals/new/', views.deal_create, name='deal_create'),
    path('deals/<int:pk>/', views.deal_detail, name='deal_detail'),
]