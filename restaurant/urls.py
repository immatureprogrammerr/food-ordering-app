from django.urls import path
from . import views
from accounts import views as account_views

urlpatterns = [
    path('', account_views.restaurant_dashboard),
    path('profile/', views.profile, name='restaurant_profile'),
    path('dashboard/', account_views.restaurant_dashboard, name='restaurant_dashboard'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>', views.products_by_category,name='products_by_category'),

    path('menu-builder/category/add', views.add_category, name='add_category'),
]