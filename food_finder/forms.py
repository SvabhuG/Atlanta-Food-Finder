from django import forms

class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Restaurant Name')
    cuisine_type = forms.CharField(required=False, label='Cuisine Type')
    location = forms.CharField(required=False, label='Location')
    min_rating = forms.DecimalField(required=False, label='Min Rating', max_digits=3, decimal_places=1)
    max_distance = forms.FloatField(required=False, label='Max Distance')


