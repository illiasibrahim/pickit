# from vendor.views import brand_view, category_view
from django.db import models
from math import ceil,floor
from imagekit import processors
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

class Category(models.Model):
    category_name   = models.CharField(max_length=50,unique=True)
    cat_image       = models.ImageField(upload_to = 'photos/categories')
    cat_offer       = models.IntegerField(default=0)
    time_added      = models.DateTimeField(auto_now_add=True)

    category_thumbnail    = ImageSpecField(
                                        source='cat_image',
                                        processors=[ResizeToFill(150,150)],
                                        format='JPEG',
                                        options={'quality':70}
                                        )

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
    offer           = models.IntegerField(default=0)
    quantity        = models.CharField(max_length=10)
    description     = models.TextField(blank=True)
    brand           = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_1         = models.ImageField(upload_to = 'photos/products/primary')
    image_2         = models.ImageField(upload_to = 'photos/products/secondary')
    image_3         = models.ImageField(upload_to = 'photos/products/secondary', blank = True)
    image_4         = models.ImageField(upload_to = 'photos/products/secondary', blank = True)
    added_at        = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)

    image_1_big_thumbnail    = ImageSpecField(
                                        source='image_1',
                                        processors=[ResizeToFill(170,170)],
                                        format='JPEG',
                                        options={'quality':85}
                                        )

    image_1_small_thumbnail    = ImageSpecField(
                                        source='image_1',
                                        processors=[ResizeToFill(140,140)],
                                        format='JPEG',
                                        options={'quality':70}
                                        )

    image_2_thumbnail    = ImageSpecField(
                                        source='image_2',
                                        processors=[ResizeToFill(100,100)],
                                        format='JPEG',
                                        options={'quality':70}
                                        )

    image_3_thumbnail    = ImageSpecField(
                                        source='image_3',
                                        processors=[ResizeToFill(100,100)],
                                        format='JPEG',
                                        options={'quality':70}
                                        )
            
    image_4_thumbnail    = ImageSpecField(
                                        source='image_4',
                                        processors=[ResizeToFill(100,100)],
                                        format='JPEG',
                                        options={'quality':70}
                                        )

    def selling_price(self):
        if (self.category.cat_offer > self.offer):
            selling_price = self.mrp * (1-(int(self.category.cat_offer)/100))
        else:
            selling_price = self.mrp * (1-(int(self.offer)/100))
        return ceil(selling_price)
    
    def discount_amount(self):
        if (self.category.cat_offer > self.offer):
            discount_amount = self.mrp * ((int(self.category.cat_offer)/100))
        else:
            discount_amount = self.mrp * ((int(self.offer)/100))
        return floor(discount_amount)

    def __str__(self):
        return self.product_name
    
    


class Banner(models.Model):
    banner_title        = models.CharField(max_length=50)
    banner              = models.ImageField(upload_to = 'photos/banner')
    added_at            = models.DateTimeField(auto_now_add=True)
    status              = models.BooleanField(default=True)

    banner_thumbnail    = ImageSpecField(
                                        source='banner',
                                        processors=[ResizeToFill(400,76)],
                                        format='JPEG',
                                        options={'quality':50}
                                        )

    def __str__(self):
        return self.banner_title

class Poster(models.Model):
    poster_name     = models.CharField(max_length=40)
    poster          = models.ImageField(upload_to = 'photos/poster')
    added_at        = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    poster_thumbnail    = ImageSpecField(
                                        source='poster',
                                        processors=[ResizeToFill(400,233)],
                                        format='JPEG',
                                        options={'quality':50}
                                        )

    def __str__(self):
        return self.poster_name