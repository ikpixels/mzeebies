from . import views
from django.urls import path

app_name = "index"

urlpatterns = [
    path('',views.index,name="index"),
    path('contact/',views.contact,name="contact"),
    path('needed_items/',views.place_order_list,name="place_order_list"),
    path('needed_item/<CATE>/',views.place_order_list,name="place_order_list2"),
    path('main_needed_item_view/',views.main_needed_item_view,name='main_needed_item_view'),
    path('edit_needed_item_form/<int:id>/',views.edit_needed_item_form,name="edit_needed_item_form"),
    path('about/',views.about,name="about"),
    path('subscribe/',views.Subscribe,name="Subscribe"),
    path('unsubscribe/',views.unsubscribe,name="unsubscribe"),
    path('terms_conditions/',views.terms_conditions,name="terms_conditions")
]
