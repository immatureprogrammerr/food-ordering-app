from django.urls import path, include
from . import views
from accounts import views as account_views

urlpatterns = [
    path('', account_views.restaurant_dashboard),
    path('profile/', views.profile, name='restaurant_profile'),
    path('dashboard/', account_views.restaurant_dashboard, name='restaurant_dashboard'),
]