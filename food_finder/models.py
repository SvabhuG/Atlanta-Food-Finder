from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    distance = models.FloatField()

    def __str__(self):
        return self.name


class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=255, unique=True)  # Unique identifier from Google Places API
    restaurant_name = models.CharField(max_length=255)
    restaurant_address = models.CharField(max_length=255)
    restaurant_rating = models.FloatField()
    restaurant_photo_reference = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  # Allow latitude to be nullable
    longitude = models.FloatField(null=True, blank=True)  # Allow longitude to be nullable
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # New field for contact number

    def __str__(self):
        return f"{self.restaurant_name} (Favorited by {self.user.username})"



class RestaurantGeolocation(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Restaurant")  # Default restaurant name
    address = models.CharField(max_length=255, default="Unknown Address")  # Default address
    latitude = models.FloatField(default=0.0)  # Default latitude
    longitude = models.FloatField(default=0.0)  # Default longitude
    details = models.TextField(default="No details available.")  # Default details

    def __str__(self):
        return self.name  # This returns the name when the model object is called


class Review(models.Model):
    favorite_restaurant = models.ForeignKey(FavoriteRestaurant, related_name='reviews', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255)
    rating = models.FloatField()
    text = models.TextField()
    relative_time_description = models.CharField(max_length=255)

    def __str__(self):
        return f"Review by {self.author_name} for {self.favorite_restaurant.restaurant_name}"
