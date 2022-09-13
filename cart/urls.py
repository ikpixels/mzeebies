from . import views
from django.urls import path

app_name = "cart"

urlpatterns = [
    path('cart/',views.shopingcart,name="cart"),
    path('add_to_cart/<slug>/',views.add_to_cart,name="add_to_cart"),
    path('cart_view/',views.cart_view,name="cart_view"),
    path('remove_cart/<int:id>/',views.remove_cart,name="remove_cart"),
    path('billing/<int:id>/',views.billing,name="billing"),
    path('paypal/<int:id>/',views.paypal,name="paypal"),
    path('stripe/<int:id>/',views.stripe,name="stripe"),
    path('charge/',views.charge_d,name="charge"),
    path('paypal_thax/',views.paypal_thax,name="paypal_thax"),
    path('delivered/',views.delivered,name="delivered"),
    path('Payment_verification/',views.confirm_mobile_payments,name="verify_p"),
    path('Payment_verification/<args>/',views.confirm_mobile_payments,name="verify_p2")
]
