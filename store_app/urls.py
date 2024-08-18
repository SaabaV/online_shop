from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('payment/', views.payment_page, name='payment_page'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('cancel/', views.cancel, name='cancel'),
    path('sale/', views.sale, name='sale'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),  # Добавьте эту строку
    path('success/', views.success, name='success'),  # Добавьте эту строку
]

