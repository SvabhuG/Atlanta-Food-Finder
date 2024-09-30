from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm
import requests
from django.shortcuts import render

API_KEY = 'AIzaSyCiFCKBxiMijE5OFYsQwslMx7VM6VEFmX0'

# def search_restaurants(request):
#     form = RestaurantSearchForm(request.GET or None)
#     restaurants = Restaurant.objects.all()
#
#     if form.is_valid():
#         if form.cleaned_data['name']:
#             restaurants = restaurants.filter(name__icontains=form.cleaned_data['name'])
#         if form.cleaned_data['cuisine_type']:
#             restaurants = restaurants.filter(cuisine_type__icontains=form.cleaned_data['cuisine_type'])
#         if form.cleaned_data['location']:
#             restaurants = restaurants.filter(location__icontains=form.cleaned_data['location'])
#         if form.cleaned_data['min_rating']:
#             restaurants = restaurants.filter(rating__gte=form.cleaned_data['min_rating'])
#         if form.cleaned_data['max_distance']:
#             restaurants = restaurants.filter(distance__lte=form.cleaned_data['max_distance'])
#
#     context = {
#         'form': form,
#         'restaurants': restaurants
#     }
#
#     return render(request, 'restaurant/search_results.html', context)
#
#
# import requests
# from django.shortcuts import render
#
# API_KEY = 'your_google_api_key'  # Replace with your API key


import requests
from django.shortcuts import render

API_KEY = 'AIzaSyCiFCKBxiMijE5OFYsQwslMx7VM6VEFmX0'  # Replace with your API key


def search_restaurants(request):
    query = request.GET.get('query', '')  # This could be restaurant name or cuisine type
    location = request.GET.get('location', 'Atlanta')  # Default location if none provided

    # Call the Google Places API
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}+restaurants&location={location}&radius=5000&key={API_KEY}"
    response = requests.get(url)

    # Print the raw JSON response to the console
    print(response.json())  # This will print the response in the terminal

    # Extract places from the response
    places = response.json().get('results', [])

    context = {
        'places': places,
        'query': query,
        'location': location
    }

    return render(request, 'restaurant/search_results.html', context)
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