# ...existing code...
from django.test import TestCase, Client
from django.urls import reverse

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_and_login(self):
        signup_url = reverse('signup')
        login_url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass123'}
        # Signup
        response = self.client.post(signup_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        # Login
        response = self.client.post(login_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
