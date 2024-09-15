from django.shortcuts import render

from .models import Restaurant
from django.http import JsonResponse
# Create your views here.

def restaurant_data(request):
    restaurants = Restaurant.objects.all()

    restaurant_list = [
        {
        "name" : restaurant.name,
        "lat" : restaurant.latitude,
        "long" : restaurant.longitude,
        "info" : restaurant.detais
    }
    for restaurant in restaurants
    ]

    return JsonResponse(restaurant_list, safe=False)