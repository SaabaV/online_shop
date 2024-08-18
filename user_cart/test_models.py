from django.test import TestCase
from store_app.models import Product, Category
from user_cart.models import Cart, CartItem, Order, ShippingAddress
from user_authorization.models import User
from django.utils import timezone


class CartModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

        # Создаем категорию для продуктов
        self.category = Category.objects.create(name='Test Category')

        # Создаем продукт с категорией
        self.product = Product.objects.create(name='Test Product', price=100, category=self.category)

        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2, price=100)

    def test_cart_total_cost(self):
        self.assertEqual(self.cart.get_total_cost(), 200)

    def test_order_creation(self):
        shipping_address = ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            city='Anytown',
            postal_code='12345',
            country='USA'
        )
        order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address='123 Main St, Anytown, USA',
            total_price=200,
            shipping_address=shipping_address,
            status='pending',
            created_at=timezone.now()
        )
        self.assertEqual(order.__str__(), f"Order {order.order_number} by John Doe")
        self.assertEqual(order.total_price, 200)

