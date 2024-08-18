from django.contrib import admin
from .models import Product, Category
from reviews.models import Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_percentage', 'discounted_price')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    readonly_fields = ('discounted_price',)  # Поле со скидкой только для чтения


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'user', 'rating')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('user', 'product', 'rating', 'created_at')  # Эти поля только для чтения


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Review, ReviewAdmin)



