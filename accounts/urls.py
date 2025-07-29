from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_account),
    path('registerUser/', views.register_user, name='registerUser'),
    path('registerRestaurant/', views.register_restaurant, name='registerRestaurant'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customer', views.customer_dashboard, name='customerDashboard'),
    path('myAccount/', views.my_account, name='myAccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgot_password, name='forgotPassword'),
    path('resetPassword/', views.reset_password, name='resetPassword'),
    path('validateResetPassword/<uidb64>/<token>/', views.validate_reset_password, name='validateResetPassword'),
    path('restaurant/', include('restaurant.urls'))
]