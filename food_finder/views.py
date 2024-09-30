import requests

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

from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import RestaurantGeolocation

# Existing restaurant data view
def restaurant_data(request):
    search_query = request.GET.get('name', '')
    if search_query:
        restaurants = RestaurantGeolocation.objects.filter(name__icontains=search_query)
    else:
        restaurants = RestaurantGeolocation.objects.all()

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

# Existing map view
def show_map(request):
    return render(request, 'map.html')  # Path to your HTML template

# New user registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in after registration
            return redirect('show_map')  # Redirect to map or home page after registration
    else:
        form = UserCreationForm()  # Create an empty form instance

    return render(request, 'register.html', {'form': form})  # Render the registration template
