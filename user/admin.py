from django.contrib import admin
from .models import Account, Cart, CartItem


# Register your models here.

admin.site.register(Account)

admin.site.register(Cart)

admin.site.register(CartItem)