from django.contrib import admin
from .models import Account, Cart, CartItem, DeliveryAddress


# Register your models here.

admin.site.register(Account)

admin.site.register(Cart)

admin.site.register(CartItem)

admin.site.register(DeliveryAddress)