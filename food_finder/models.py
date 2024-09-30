
# Create your models here.
from django.db import models
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
class Restaurant_geolocation(models.Model):
    name = models.CharField(max_length=255)  # Stores the restaurant's name
    address = models.CharField(max_length=255)  # Stores the restaurant's address
    latitude = models.FloatField()  # Latitude for the map
    longitude = models.FloatField()  # Longitude for the map
    details = models.TextField()  # Additional information

    def __str__(self):
        return self.name  # This returns the name when the model object is called

class RestaurantGeolocation(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Restaurant")  # Default restaurant name
    address = models.CharField(max_length=255, default="Unknown Address")  # Default address
    latitude = models.FloatField(default=0.0)  # Default latitude
    longitude = models.FloatField(default=0.0)  # Default longitude
    details = models.TextField(default="No details available.")  # Default details

    def __str__(self):
        return self.name  # This returns the name when the model object is called


#used to track the likes of each user
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # default user fields
    restaurant = models.ForeignKey(RestaurantGeolocation, on_delete=models.CASCADE) #the restaurant they liked
    liked_at = models.DateTimeField(auto_now_add=True) #time the liked at

    def __str__(self):
        return f'{self.user.username} liked {self.restaurant.name}'

