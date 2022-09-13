from . import views
from django.urls import path

app_name = "account"

urlpatterns = [
    path('dashboard/',views.Dashboard,name="dashboard"),
    path('dashboard/<args>/',views.Dashboard,name="Dashboard2"),
    path('login/',views.login_view,name="google_login"),
    path('bill/',views.bill,name="bill"),
    path('change_password/',views.change_password,name="change_password"),
    path('register/',views.register_view,name="register_view"),
    path('logout/',views.logout_view,name="logout_view"),
    path('cart_detail/',views.cart_detail,name="cart_detail"),
    path('my_account/',views.customer_account,name="customer_account"),
    path('my_account/<args>/',views.customer_account,name="customer_account2")
]
