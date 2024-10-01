import requests
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import RestaurantGeolocation, FavoriteRestaurant, Review  # Import the Review model
from django.contrib.auth.decorators import login_required
from django.conf import settings


API_KEY = settings.GOOGLE_MAPS_API_KEY  # Retrieve the API key from your settings


@login_required
def search_restaurants(request):
    query = request.GET.get('query', '')  # This could be restaurant name or cuisine type
    location = request.GET.get('location', 'Atlanta')  # Default location if none provided

    # Retrieve the API key from settings
    API_KEY = settings.GOOGLE_MAPS_API_KEY

    # Call the Google Places Text Search API
    text_search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}+restaurants&location={location}&radius=5000&key={API_KEY}"
    response = requests.get(text_search_url)

    # Extract places from the response
    places = response.json().get('results', [])

    # List to store places along with reviews and details
    places_with_details = []

    # Get the list of liked place_ids for the current user
    liked_restaurants = FavoriteRestaurant.objects.filter(user=request.user).values_list('place_id', flat=True)

    # Call Place Details API to get reviews, phone numbers, and cuisine type for each place
    for place in places:
        place_id = place.get('place_id')

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
        else:
            # Otherwise, add it to the favorites
            # Fetch details from the Google Places API (including cuisine type)
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews,formatted_phone_number,types&key={API_KEY}"
            details_response = requests.get(details_url)
            details_data = details_response.json()

            # Check if reviews exist in the details response
            reviews = details_data.get('result', {}).get('reviews', [])
            phone_number = details_data.get('result', {}).get('formatted_phone_number', 'N/A')

            favorite_restaurant = FavoriteRestaurant.objects.create(
                user=request.user,
                place_id=place_id,
                restaurant_name=restaurant_name,
                restaurant_address=restaurant_address,
                restaurant_rating=restaurant_rating,
                restaurant_photo_reference=restaurant_photo_reference,
                latitude=latitude,
                longitude=longitude,
                phone_number=phone_number,  # Store the phone number
            )

            # Create Review objects for each review in the response
            for review_data in reviews:
                Review.objects.create(
                    favorite_restaurant=favorite_restaurant,
                    author_name=review_data['author_name'],
                    rating=review_data['rating'],
                    text=review_data['text'],
                    relative_time_description=review_data['relative_time_description']
                )

    return redirect('search_restaurants')


@login_required
def favorite_restaurants(request):
    # Get the list of liked restaurants for the current user
    favorite_restaurants = FavoriteRestaurant.objects.filter(user=request.user)

    # Prepare restaurant data with latitude and longitude for the map
    restaurant_data = [
        {
            'restaurant': favorite,
            'latitude': favorite.latitude,  # Assuming latitude is stored
            'longitude': favorite.longitude  # Assuming longitude is stored
        }
        for favorite in favorite_restaurants
    ]

    context = {
        'favorite_restaurants': restaurant_data,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,  # Pass the API key to the template
    }

    return render(request, 'restaurant/favorite_restaurants.html', context)


@login_required
def unlike_restaurant(request, favorite_id):
    favorite = get_object_or_404(FavoriteRestaurant, id=favorite_id, user=request.user)
    favorite.delete()  # Remove the favorite restaurant
    return redirect('favorite_restaurants')  # Redirect back to the favorite restaurants list


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
