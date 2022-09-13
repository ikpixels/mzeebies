from . import views
from django.urls import path

app_name = "vendor"

urlpatterns = [
    path('become_vendor/',views.Vendor,name="vendor"),
    path('vendor_db/',views.vendor_db,name='vendor_db'),
    path('add_agent/',views.add_agent,name="agent"),
    path('deal_payment_verification/',views.deal_payment_verification,name="deal_payment_verification"),
    path('edit_agent/<int:id>/',views.add_agent,name="edit_agent"),
    path('bill_payment/<plan>/',views.billPayment,name="bill_payment"),
    path('edit_vendor_account/<int:id>/',views.EditVendor,name="edit_vendor"),
    path('vendor/',views.welcome_remarks,name="welcome_remarks"),
    path('vendor_account/',views.vendor_account,name="vendor_account"),
    path('items_sold/',views.items_sold,name="items_sold"),
    path('payment_feedback/',views.payment_feedback,name="payment_feedback"),
    path('bill_verification/',views.bill_verification,name="bill_verification")
  
]
