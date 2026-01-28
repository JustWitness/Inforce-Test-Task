from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Menu

User = get_user_model()


# Create your tests here.
class MenuSystemTests(APITestCase):

    def setUp(self):
        self.menu_url = reverse('menu')  # Matches MenuAPIView
        self.available_url = reverse('menu-available')  # Matches AvailableMenusAPIView
        self.vote_url = reverse('menu-vote')  # Matches MenuVoteAPIView
        self.results_url = reverse('menu-winner')  # Matches MenuResultsAPIView

        self.restaurant1 = User.objects.create(
            username="test-restaurant-1", email="restaurant1@test.com", password="password123", role="RESTAURANT"
        )
        self.restaurant2 = User.objects.create(
            username="test-restaurant-2", email="restaurant2@test.com", password="password123", role="RESTAURANT"
        )
        self.employee = User.objects.create(
            username="test-employee", email="employee@test.com", password="password123", role="EMPLOYEE"
        )

    def test_restaurant_can_create_menu(self):
        self.client.force_authenticate(user=self.restaurant1)
        data = {
            "name": "Pizza Day",
            "date": timezone.localdate(),
            "items": [{"name": "Margherita", "description": "Pizza", "price": 10.00}]
        }
        # Note: Added format="json" to avoid the 400 error we saw earlier!
        response = self.client.post(self.menu_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)

    def test_employee_cannot_create_menu(self):
        self.client.force_authenticate(user=self.employee)
        data = {"name": "Hacker Menu"}
        response = self.client.post(self.menu_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_vote(self):
        menu = Menu.objects.create(restaurant=self.restaurant1, name="Pasta Day", date=timezone.localdate())

        self.client.force_authenticate(user=self.employee)
        data = {"menu": menu.id, "employee": self.employee.id}
        response = self.client.post(self.vote_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_winner(self):
        Menu.objects.create(restaurant=self.restaurant1, name="Menu A", date=timezone.localdate())
        Menu.objects.create(restaurant=self.restaurant2, name="Menu B", date=timezone.localdate())

        self.client.force_authenticate(user=self.employee)
        response = self.client.get(self.results_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
