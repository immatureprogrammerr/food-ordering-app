def detect_user(user):
    redirect_url = ''
    if user.role == 1:
        redirect_url = 'restaurantDashboard'
    elif user.role == 2:
        redirect_url = 'customerDashboard'
    elif user.role is None and user.is_superadmin:
        redirect_url = 'admin'
    return redirect_url