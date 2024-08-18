from django.test import TestCase, Client
from django.urls import reverse
from store_app.models import Product, Category  # Импортируем модель Category
from user_cart.models import Cart, CartItem, Order, ShippingAddress
from user_authorization.models import User
from django.utils import timezone


class CartViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

        # Создаем категорию для продуктов
        self.category = Category.objects.create(name='Test Category')

        # Создаем продукт с категорией
        self.product = Product.objects.create(name='Test Product', price=100, category=self.category)

        self.cart_url = reverse('cart_detail')
        self.add_to_cart_url = reverse('add_to_cart', args=[self.product.id])
        self.buy_now_url = reverse('buy_now', args=[self.product.id])

    def test_cart_detail_view_authenticated_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_cart/cart_detail.html')

    def test_cart_detail_view_anonymous_user(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_cart/cart_detail.html')

    def test_add_to_cart_authenticated_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.add_to_cart_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # Redirect to cart detail
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_add_to_cart_anonymous_user(self):
        session = self.client.session
        session.save()
        response = self.client.post(self.add_to_cart_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # Redirect to cart detail
        cart = Cart.objects.get(session_id=session.session_key)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)

    def test_buy_now_authenticated_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.buy_now_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '12345',
            'country': 'USA'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to Stripe session
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.status, 'pending')

    def test_buy_now_anonymous_user(self):
        session = self.client.session
        session.save()
        response = self.client.post(self.buy_now_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '12345',
            'country': 'USA'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to Stripe session
        order = Order.objects.get(shipping_address__session_id=session.session_key)
        self.assertEqual(order.first_name, 'John')
        self.assertEqual(order.status, 'pending')

    def test_checkout_success(self):
        self.client.login(username='testuser', password='password')
        shipping_address = ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            city='Anytown',
            state='CA',
            postal_code='12345',
            country='USA'
        )
        order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address='123 Main St, Anytown, USA',
            total_price=100,
            shipping_address=shipping_address,  # Убедитесь, что адрес доставки добавлен к заказу
            status='pending',
            created_at=timezone.now()
        )

        # Проверяем, что shipping_address не None
        self.assertIsNotNone(order.shipping_address)

        response = self.client.get(reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')



