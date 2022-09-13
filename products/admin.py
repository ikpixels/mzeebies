from django.contrib import admin
from . models import Categories,item_contacts,Brand,Popular,product,category_banner,add_image

admin.site.register(Categories)
admin.site.register(product)
admin.site.register(category_banner)
admin.site.register(add_image)
admin.site.register(Popular)
admin.site.register(Brand)
admin.site.register(item_contacts)
