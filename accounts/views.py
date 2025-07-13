from django.http import HttpResponse
from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = User.CUSTOMER
            user.save()

            messages.success(request, 'You have registered successfully.')
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registeruser.html', context)

def register_restaurant(request):
    if request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = User.RESTAURANT
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user

            # getting the user profile from the user which got created via Signals
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'You have registered successfully. Please wait for the Admin approval.')
            return redirect('registerRestaurant')
        else:
            print(form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form': form,
        'vendor_form': vendor_form,
    }
    return render(request, 'accounts/registerrestaurant.html', context=context)