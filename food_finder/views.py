from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm

def search_restaurants(request):
    form = RestaurantSearchForm(request.GET or None)
    restaurants = Restaurant.objects.all()

    if form.is_valid():
        if form.cleaned_data['name']:
            restaurants = restaurants.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['cuisine_type']:
            restaurants = restaurants.filter(cuisine_type__icontains=form.cleaned_data['cuisine_type'])
        if form.cleaned_data['location']:
            restaurants = restaurants.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['min_rating']:
            restaurants = restaurants.filter(rating__gte=form.cleaned_data['min_rating'])
        if form.cleaned_data['max_distance']:
            restaurants = restaurants.filter(distance__lte=form.cleaned_data['max_distance'])

    context = {
        'form': form,
        'restaurants': restaurants
    }

    return render(request, 'restaurant/search_results.html', context)
