from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from accounts.views import check_role_restaurant
from restaurant.forms import RestaurantForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Restaurant
from django.contrib import messages

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    restaurant = get_object_or_404(Restaurant, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance=restaurant)

        if profile_form.is_valid() and restaurant_form.is_valid():
            profile_form.save()
            restaurant_form.save()
            messages.success(request, 'Restaurant has been updated.')
            return redirect('restaurant_profile')
        else:
            print(restaurant_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Some error occurred.')
            return redirect('restaurant_profile')

    profile_form = UserProfileForm(instance = profile)
    restaurant_form = RestaurantForm(instance = restaurant)

    context = {
        'profile_form': profile_form,
        'restaurant_form': restaurant_form,
        'profile': profile,
        'restaurant': restaurant,
    }
    return render(request, 'restaurant/restaurant_profile.html', context)