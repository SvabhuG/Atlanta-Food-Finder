# Generated by Django 4.2.15 on 2024-10-02 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food_finder', '0005_remove_favoriterestaurant_cuisine_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name="favoriterestaurant",
            name="latitude",
        ),
        migrations.RemoveField(
            model_name="favoriterestaurant",
            name="longitude",
        ),
    ]
