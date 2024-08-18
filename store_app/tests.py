from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .models import Product, Category
from .utils import round_price_to_99_cents

class StoreAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal("100.00"),
            category=self.category,
            color="Blue-white",
            discount_percentage=10
        )

    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_app/home.html')
        self.assertIn(self.product, response.context['products'])

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_app/product_detail.html')
        self.assertEqual(response.context['product'], self.product)

    def test_sale_page_view(self):
        response = self.client.get(reverse('sale'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_app/sale.html')
        self.assertIn(self.product, response.context['products'])

    def test_about_page_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store_app/about.html')

    def test_product_creation(self):
        response = self.client.post(reverse('product_create'), {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '10.00',
            'category': self.category.id,
            'color': 'Blue-white'
        })

        # Выведите ошибки формы, если они есть
        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

    def test_round_price_to_99_cents(self):
        price = Decimal('99.49')
        rounded_price = round_price_to_99_cents(price)
        self.assertEqual(rounded_price, Decimal('99.99'))

    def test_process_payment(self):
        cart = {
            str(self.product.id): {
                'name': self.product.name,
                'price': float(self.product.price),
                'quantity': 1,
            }
        }
        session = self.client.session
        session['cart'] = cart
        session.save()

        response = self.client.post(reverse('process_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())

    def test_success_view(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_cart/checkout_success.html')

    def test_cancel_view(self):
        response = self.client.get(reverse('cancel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_cart/checkout_cancel.html')
