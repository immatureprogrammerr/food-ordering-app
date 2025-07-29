from django import forms
from restaurant.models import Restaurant

class RestaurantForm(forms.ModelForm):
    restaurant_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}))
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_license']