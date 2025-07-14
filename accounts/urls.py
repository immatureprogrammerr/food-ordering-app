from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.register_user, name='registerUser'),
    path('registerRestaurant/', views.register_restaurant, name='registerRestaurant'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customerDashboard', views.customer_dashboard, name='customerDashboard'),
    path('restaurantDashboard', views.restaurant_dashboard, name='restaurantDashboard'),
    path('myAccount', views.my_account, name='myAccount'),
]