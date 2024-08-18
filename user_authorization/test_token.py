from django.test import TestCase
from user_authorization.token import create_access_token, verify_token, decode_access_token
from jose import JWTError

class TokenTests(TestCase):

    def setUp(self):
        self.user_data = {"user_id": "123"}
        self.token = create_access_token(self.user_data)

    def test_create_access_token(self):
        self.assertIsNotNone(self.token)

    def test_verify_token(self):
        credentials_exception = Exception("Credentials Exception")
        decoded_data = verify_token(self.token, credentials_exception)
        self.assertEqual(decoded_data['user_id'], self.user_data['user_id'])

    def test_decode_access_token(self):
        decoded_data = decode_access_token(self.token)
        self.assertEqual(decoded_data['user_id'], self.user_data['user_id'])

    def test_invalid_token(self):
        invalid_token = self.token + "invalid"  # Добавляем недействительную часть к токену
        credentials_exception = JWTError("Invalid token")  # Используем JWTError как credentials_exception
        with self.assertRaises(JWTError):
            verify_token(invalid_token, credentials_exception)

