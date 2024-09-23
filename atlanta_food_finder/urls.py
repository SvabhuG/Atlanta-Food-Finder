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

from food_finder import views

urlpatterns = [
    path('map/', views.show_map, name='show_map'),
    path('api/restaurants/', views.restaurant_data, name='restaurant_data'),  # API for fetching restaurant data
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Include allauth routes for login, registration, etc.
]

