from django.test import TestCase
from .models import Restaurant
from django.urls import reverse

class RestaurantSearchTest(TestCase):

    def setUp(self):
        # Create some fake restaurants
        Restaurant.objects.create(name="Pizza Palace", cuisine_type="Italian", location="Atlanta", rating=4.5, distance=5)
        Restaurant.objects.create(name="Sushi World", cuisine_type="Japanese", location="New York", rating=4.8, distance=10)
        Restaurant.objects.create(name="Burger Town", cuisine_type="American", location="San Francisco", rating=3.8, distance=15)

    def test_search_by_name(self):
        response = self.client.get(reverse('search_restaurants'), {'name': 'Pizza'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza Palace')

    def test_search_by_cuisine_type(self):
        response = self.client.get(reverse('search_restaurants'), {'cuisine_type': 'Japanese'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sushi World')

    def test_search_by_location(self):
        response = self.client.get(reverse('search_restaurants'), {'location': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sushi World')

    def test_search_by_rating(self):
        response = self.client.get(reverse('search_restaurants'), {'min_rating': 4.0})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza Palace')
        self.assertContains(response, 'Sushi World')
        self.assertNotContains(response, 'Burger Town')

    def test_search_by_distance(self):
        response = self.client.get(reverse('search_restaurants'), {'max_distance': 10})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pizza Palace')
        self.assertContains(response, 'Sushi World')
        self.assertNotContains(response, 'Burger Town')
