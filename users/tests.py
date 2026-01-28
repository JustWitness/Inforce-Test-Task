from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Create your tests here.
class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register-user')  # Change to your actual URL name
        self.login_url = reverse('login-user')  # Change to your actual URL name
        self.logout_url = reverse('logout-user')  # Change to your actual URL name

        self.user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "password123",
            "role": "EMPLOYEE"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_registration(self):
        new_user_data = {
            "username": "newuser",
            "email": "new@test.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "RESTAURANT",
            "password1": "password123",
            "password2": "password123",
        }
        response = self.client.post(self.register_url, new_user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertEqual(User.objects.filter(username="newuser").count(), 1)

    def test_login(self):
        data = {
            "email": "test@test.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertTrue(response.data['username'] == "testuser")

    def test_logout(self):
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}

        response = self.client.post(self.logout_url, data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        try:
            RefreshToken(str(refresh))
        except Exception:
            pass

    def test_login_invalid_credentials(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
