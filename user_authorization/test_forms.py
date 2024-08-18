from django.test import TestCase
from user_authorization.forms import RegistrationForm


class RegistrationFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'address': '123 Main St',
            'house_number': '10',
            'city': 'Anytown',
            'postal_code': '12345',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': '',
            'email': 'testuser@example.com',
            'address': '123 Main St',
            'house_number': '',
            'city': 'Anytown',
            'postal_code': '',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('house_number', form.errors)
        self.assertIn('postal_code', form.errors)
