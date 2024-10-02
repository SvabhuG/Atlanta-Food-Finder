import requests
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import FavoriteRestaurant, RestaurantGeolocation
from django.contrib.auth.decorators import login_required
from django.conf import settings
from geopy.distance import geodesic  # To calculate distance between two coordinates

API_KEY = settings.GOOGLE_MAPS_API_KEY  # Retrieve the API key from your settings

@login_required
def search_restaurants(request):
    query = request.GET.get('query', '')  # This could be restaurant name or cuisine type
    location = request.GET.get('location', '33.7490,-84.3880')  # Default to Atlanta coordinates (lat, lng)
    rating_filter = request.GET.get('rating', '')  # Get the rating filter
    distance_filter = request.GET.get('distance', '')  # Get the distance filter in miles

    # Call the Google Places Text Search API
    text_search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}+restaurants&location={location}&radius=5000&key={API_KEY}"
    response = requests.get(text_search_url)
    places = response.json().get('results', [])

    # List to store places along with reviews and details
    places_with_details = []
    user_location = tuple(map(float, location.split(',')))  # Convert location to (lat, lng)

    # Get the list of liked place_ids for the current user
    liked_restaurants = FavoriteRestaurant.objects.filter(user=request.user).values_list('place_id', flat=True)

    # Call Place Details API to get reviews, phone numbers, and cuisine type for each place
    for place in places:
        place_id = place.get('place_id')

        # Apply the rating filter
        if rating_filter and place.get('rating', 0) < float(rating_filter):
            continue  # Skip places that don't meet the rating filter

        # Calculate distance between user's location and restaurant location
        place_location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
        distance = geodesic(user_location, place_location).miles

        # Apply the distance filter
        if distance_filter and distance > float(distance_filter):
            continue  # Skip places that don't meet the distance filter

        # Call Google Places Details API to fetch reviews, phone number, and cuisine type
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews,formatted_phone_number,types&key={API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        # Extract reviews and phone number
        reviews = details_data.get('result', {}).get('reviews', [])
        phone_number = details_data.get('result', {}).get('formatted_phone_number', 'N/A')

        # Limit the number of reviews to 2
        limited_reviews = reviews[:2]

        # Add phone number, cuisine type, and reviews to the current place
        place['reviews'] = limited_reviews
        place['phone_number'] = phone_number
        place['distance'] = round(distance, 2)  # Add calculated distance to the place

        # Add the place with details to the list
        places_with_details.append(place)

    context = {
        'places': places_with_details,
        'query': query,
        'location': location,
        'liked_restaurants': liked_restaurants,
        'google_maps_api_key': API_KEY,  # Pass the API key to the template
    }

    return render(request, 'restaurant/search_results.html', context)

@login_required
def like_restaurant(request):
    if request.method == 'POST':
        place_id = request.POST.get('place_id')
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_address = request.POST.get('restaurant_address')
        restaurant_rating = request.POST.get('restaurant_rating')
        restaurant_photo_reference = request.POST.get('restaurant_photo_reference')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Check if the user has already liked this restaurant (based on place_id)
        existing_favorite = FavoriteRestaurant.objects.filter(user=request.user, place_id=place_id)

        if existing_favorite.exists():
            # If already liked, remove it (unlike)
            existing_favorite.delete()
            liked = False
        else:
            # Otherwise, add it to the favorites
            FavoriteRestaurant.objects.create(
                user=request.user,
                place_id=place_id,
                restaurant_name=restaurant_name,
                restaurant_address=restaurant_address,
                restaurant_rating=restaurant_rating,
                restaurant_photo_reference=restaurant_photo_reference,
                latitude=latitude,
                longitude=longitude
            )
            liked = True

        return JsonResponse({'liked': liked})

@login_required
def favorite_restaurants(request):
    favorite_restaurants = FavoriteRestaurant.objects.filter(user=request.user)

    restaurant_data = []

    for favorite in favorite_restaurants:
        # Fetch details from the Google Places API (including reviews and phone number)
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={favorite.place_id}&fields=reviews,formatted_phone_number&key={settings.GOOGLE_MAPS_API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        # Check if reviews exist in the details response
        reviews = details_data.get('result', {}).get('reviews', [])
        phone_number = details_data.get('result', {}).get('formatted_phone_number', 'N/A')

        restaurant_data.append({
            'restaurant': favorite,
            'reviews': reviews,
            'phone_number': phone_number
        })

    context = {
        'restaurant_data': restaurant_data,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }

    return render(request, 'restaurant/favorite_restaurants.html', context)

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

@login_required
def unlike_restaurant(request, favorite_id):
    favorite = get_object_or_404(FavoriteRestaurant, id=favorite_id, user=request.user)
    favorite.delete()  # Remove the favorite restaurant
    return redirect('favorite_restaurants')  # Redirect back to the favorite restaurants list
