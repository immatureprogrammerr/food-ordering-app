from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth

from .utils import detect_user
from django.core.exceptions import PermissionDenied

# Restrict the restaurant from accessing the customer page
def check_role_restaurant(user):
    if user.role == 1:
        return True
    raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied

def register_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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
    if request.user.is_authenticated:
        return redirect('dashboard')
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

def login(request):
    if request.user.is_authenticated:
        return redirect('myAccount')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have logged-in successfully')
            return redirect('myAccount')
        else:
            messages.error(request, 'Username/password incorrect!')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_restaurant)
def restaurant_dashboard(request):
    return render(request, 'accounts/restaurant_dashboard.html')

@login_required(login_url='login')
def my_account(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)