from django.contrib.admin.options import ModelAdmin
from vendor.models import Category
from django.contrib import admin
from .models import Category, Brand, Banner, Product, Poster
# Register your models here.



admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Poster)

admin.site.register(Banner)

admin.site.register(Brand)