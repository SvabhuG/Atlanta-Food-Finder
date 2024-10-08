"""
URL configuration for atlanta_food_finder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from food_finder import views

urlpatterns = [
    path('api/restaurants/', views.restaurant_data, name='restaurant_data'),  # API for fetching restaurant data
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Include allauth routes for login, registration, etc.
    path('search/', views.search_restaurants, name='search_restaurants'),
    path('like/', views.like_restaurant, name='like_restaurant'),
    path('favorites/', views.favorite_restaurants, name='favorite_restaurants'),
    path('unlike/<int:favorite_id>/', views.unlike_restaurant, name='unlike_restaurant'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

