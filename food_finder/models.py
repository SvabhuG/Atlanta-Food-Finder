
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)  # Stores the restaurant's name
    address = models.CharField(max_length=255)  # Stores the restaurant's address
    latitude = models.FloatField()  # Latitude for the map
    longitude = models.FloatField()  # Longitude for the map
    details = models.TextField()  # Additional information

    def __str__(self):
        return self.name  # This returns the name when the model object is called

