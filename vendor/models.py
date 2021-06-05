
# from vendor.views import brand_view, category_view
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name   = models.CharField(max_length=50,unique=True)
    cat_image       = models.ImageField(upload_to = 'photos/categories')
    time_added      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name   = models.CharField(max_length=50,unique=True)
    time_added   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_name    = models.CharField(max_length=100, unique=True)
    mrp             = models.IntegerField()
    offer           = models.IntegerField()
    discount        = models.IntegerField(default=0)
    discount_price  = models.IntegerField(default=0)
    quantity        = models.CharField(max_length=10)
    brand           = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_1         = models.ImageField(upload_to = 'photos/products/primary')
    image_2         = models.ImageField(upload_to = 'photos/products/secondary')
    image_3         = models.ImageField(upload_to = 'photos/products/secondary', blank = True)
    image_4         = models.ImageField(upload_to = 'photos/products/secondary', blank = True)
    added_at        = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Banner(models.Model):
    banner_title    = models.CharField(max_length=50, unique=True)
    banner          = models.ImageField(upload_to = 'photos/banner')
    added_at        = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.banner_title

class Poster(models.Model):
    poster_name     = models.CharField(max_length=40, unique=True)
    poster          = models.ImageField(upload_to = 'photos/poster')
    added_at        = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.poster_name