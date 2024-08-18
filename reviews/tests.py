from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from store_app.models import Product, Category
from user_cart.models import Purchase
from reviews.models import Review
from django.contrib.messages import get_messages

User = get_user_model()

class ReviewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            category=self.category
        )
        self.purchase = Purchase.objects.create(user=self.user, product=self.product)
        self.add_review_url = reverse('add_review', args=[self.product.id])

    def test_add_review_success(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.add_review_url, {
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошло перенаправление
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())  # Проверяем, что отзыв создан

    def test_add_review_without_purchase(self):
        self.client.login(username='testuser', password='password')
        # Удаляем покупку, чтобы проверить невозможность оставить отзыв без покупки
        self.purchase.delete()
        response = self.client.post(self.add_review_url, {
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошло перенаправление
        self.assertFalse(
            Review.objects.filter(product=self.product, user=self.user).exists())  # Проверяем, что отзыв не создан

        # Проверка наличия сообщения об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('To leave a review, make a purchase of this product.' in str(message) for message in messages))

    def test_review_form_display(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.add_review_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="rating"')
        self.assertContains(response, 'name="comment"')

