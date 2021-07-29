from django.contrib import admin
from .models import Account, Cart, CartItem, Coupon, DefaultAddress, DeliveryAddress, ReviewRating
from .models import Payment,Order,OrderProduct
from django.utils.html import format_html


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):

    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.display_picture.url))
    thumbnail.short_description = 'Profile picture'


admin.site.register(Account)

admin.site.register(Cart)

admin.site.register(CartItem)

admin.site.register(DeliveryAddress)

admin.site.register(DefaultAddress)

admin.site.register(Payment)

admin.site.register(Order)

admin.site.register(OrderProduct)

admin.site.register(Coupon)

admin.site.register(ReviewRating)