from django.test import TestCase
from user_cart.forms import ShippingAddressForm


class ShippingAddressFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'postal_code': '12345',
            'country': 'USA'
        }
        form = ShippingAddressForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'first_name': '',
            'last_name': 'Doe',
            'address': '',
            'city': 'Anytown',
            'state': 'CA',
            'postal_code': '12345',
            'country': 'USA'
        }
        form = ShippingAddressForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Должно быть две ошибки: first_name и address
