from . import views
from django.urls import path

app_name = "products"

urlpatterns = [
    path('shop/',views.mainshop,name="mainshop"),#for main shop
    path('shop/<args_>/',views.mainshop,name="mainshop2"),# for categories
    path('mainshop22/<args_2>/',views.mainshop,name="type"),
    path('deals_payment_form/<slug>/',views.Deal_payment_form,name="deal_payment_form"),
    path('additem/<int:id>/',views.additem,name="additem"),
    path('additem_msg/',views.additem_msg,name="additem_msg"),
    path('Edit/<slug>/',views.additem,name="edit"),
    path('item_view/',views.item_view,name="item_view"),
    path('additemBanner/',views.additemBanner,name="banner"),
    path('additemBanner/<int:args>/',views.additemBanner,name="banner_edit"),
    path('detail/<slug>/',views.detail,name="detail"),
    path('additemImage/<slug>/',views.additemImage,name="additemImage"),
    path('category_v/',views.category_v,name="category_v"),
    path('upload_brand/',views.upload_brand_img,name="upload_brand"),
    path('timer/',views.timer,name="timer"),
    path('delete/<slug>/',views.delete_item,name="delete_item"),
    path('delete/<int:id>/',views.delete_brand,name="delete_brand"),
    path('remove_category/',views.remove_category,name="remove_category")

]
