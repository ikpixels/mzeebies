from django.contrib import admin
from . models import Order,Mobile,Top_seller,OrderItem,item_size_color,billing_address,shipping_address

admin.site.register(Order)
admin.site.register(OrderItem),
admin.site.register(item_size_color)
admin.site.register(billing_address)
admin.site.register(shipping_address)
admin.site.register(Top_seller)
admin.site.register(Mobile)