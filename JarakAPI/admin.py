from django.contrib import admin
from .models import Product, Profile, RentedItem

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(RentedItem)
