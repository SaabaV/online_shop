from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_authorization.forms import RegistrationForm

User = get_user_model()

class AuthorizationViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='ComplexPass123')

    def test_registration_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_registration_view_post_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'address': '123 Main St',
            'house_number': '10',
            'city': 'Anytown',
            'postal_code': '12345',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        response = self.client.post(self.register_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_view_post_invalid(self):
        form_data = {
            'username': '',
            'email': 'newuser@example.com',
            'address': '123 Main St',
            'house_number': '10',
            'city': 'Anytown',
            'postal_code': '12345',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        response = self.client.post(self.register_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'ComplexPass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_login_view_post_invalid(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'WrongPass'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIn('Invalid login credentials', response.context['form'].errors['__all__'])

    def test_logout_view(self):
        self.client.login(username='testuser', password='ComplexPass123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('welcome'))
