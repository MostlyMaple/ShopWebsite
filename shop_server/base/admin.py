from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Item)
admin.site.register(ClothingType)
admin.site.register(ClothingSize)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)