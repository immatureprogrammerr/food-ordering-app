from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from accounts.views import check_role_restaurant
from menu.models import Category, Product
from restaurant.forms import RestaurantForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Restaurant
from django.contrib import messages
from menu.forms import CategoryForm

def get_restaurant(request):
    return Restaurant.objects.get(user=request.user)

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

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def menu_builder(request):
    restaurant = get_restaurant(request)
    categories = Category.objects.filter(restaurant=restaurant)
    context = {
        'categories': categories,
    }
    return render(request, 'restaurant/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def products_by_category(request, pk=None):
    restaurant = get_restaurant(request)
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(restaurant=restaurant, category=category)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'restaurant/products_by_category.html', context)

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_data']
            category = form.save(commit=False)
            category.restaurant = get_restaurant(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('menu_builder')
        else:
            form = CategoryForm()
    form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'restaurant/add_category.html', context)