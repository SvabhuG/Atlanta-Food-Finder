from django.contrib import admin
from django.urls import path

from food_finder import views

urlpatterns = [
    path('map/', views.show_map, name='show_map'),
    path('api/restaurants/', views.restaurant_data, name='restaurant_data'),  # API for fetching restaurant data
]
