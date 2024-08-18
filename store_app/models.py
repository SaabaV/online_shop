# models.py
from django.db import models
from decimal import Decimal
from .utils import round_price_to_99_cents
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=750)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, choices=[
        ('Blue-white', 'Blue-white'),
        ('blue-burquoise', 'blue-burquoise'),
        ('pink-silver', 'pink-silver'),
        ('fillet', 'fillet'),
        ('purple-white', 'purple-white'),
        ('pearl-golden', 'pearl-golden'),
        ('blue-golden', 'blue-golden'),
    ], default='Blue-white')
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    average_rating = models.FloatField(default=0)  # Средний рейтинг
    review_count = models.IntegerField(default=0)  # Количество отзывов

    def save(self, *args, **kwargs):
        if self.discount_percentage > 0:
            discounted_price = Decimal(self.price) * (1 - Decimal(self.discount_percentage) / Decimal(100))
            self.discounted_price = round_price_to_99_cents(discounted_price)
        else:
            self.discounted_price = None  # No discount, no discounted price
        super().save(*args, **kwargs)

    def get_average_rating(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating or 0, 2)

    def __str__(self):
        return f"{self.name} ({self.color})"




