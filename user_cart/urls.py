from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('product/<int:pk>/buy_now/', views.buy_now, name='buy_now'),
    path('success/<uuid:order_id>/', views.checkout_success, name='checkout_success'),
    path('cart/success/<uuid:order_id>/', views.checkout_success, name='checkout_success'),
    path('cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('checkout/', views.create_checkout_session, name='checkout'),
]


