from django.contrib import admin
from .models import Cart, CartItem, Purchase
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'created_at', 'total_price', 'payment_date')
    list_filter = ('status',)  # Добавляет фильтр по статусу в правой части админки
    search_fields = ('order_number', 'user__username', 'shipping_address__first_name', 'shipping_address__last_name')
    ordering = ('status',)  # Добавляет сортировку по статусу по умолчанию


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [CartItemInline]


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'purchased_at')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')


admin.site.register(Cart, CartAdmin)
admin.site.register(Purchase, PurchaseAdmin)

