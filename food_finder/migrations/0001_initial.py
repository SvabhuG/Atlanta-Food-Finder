# Generated by Django 5.1.1 on 2024-10-01 22:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("cuisine_type", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("rating", models.DecimalField(decimal_places=1, max_digits=3)),
                ("distance", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="RestaurantGeolocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(default="Unnamed Restaurant", max_length=255),
                ),
                (
                    "address",
                    models.CharField(default="Unknown Address", max_length=255),
                ),
                ("latitude", models.FloatField(default=0.0)),
                ("longitude", models.FloatField(default=0.0)),
                ("details", models.TextField(default="No details available.")),
            ],
        ),
        migrations.CreateModel(
            name="FavoriteRestaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("place_id", models.CharField(max_length=255, unique=True)),
                ("restaurant_name", models.CharField(max_length=255)),
                ("restaurant_address", models.CharField(max_length=255)),
                ("restaurant_rating", models.FloatField()),
                (
                    "restaurant_photo_reference",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
