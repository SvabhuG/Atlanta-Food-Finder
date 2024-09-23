from django.shortcuts import render
from django.http import JsonResponse
from .models import Restaurant_geolocation

def restaurant_data(request):
    search_query = request.GET.get('name', '')
    if search_query:
        restaurants = Restaurant_geolocation.objects.filter(name__icontains=search_query)
    else:
        restaurants = Restaurant_geolocation.objects.all()

    restaurant_list = [
        {
            "name": restaurant.name,
            "lat": restaurant.latitude,
            "long": restaurant.longitude,
            "info": restaurant.details
        }
        for restaurant in restaurants
    ]

    return JsonResponse(restaurant_list, safe=False)

def show_map(request):
    return render(request, 'map.html')  # Path to your HTML template
