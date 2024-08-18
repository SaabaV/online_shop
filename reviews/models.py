# models.py
from django.db import models
from django.conf import settings
from store_app.models import Product


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Пересчет среднего рейтинга и количества отзывов
        reviews = Review.objects.filter(product=self.product)
        average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.product.average_rating = average_rating
        self.product.review_count = reviews.count()
        self.product.save()
