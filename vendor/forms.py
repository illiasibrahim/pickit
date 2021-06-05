from django import forms
from django.db.models import fields
from .models import Category,Brand, Poster,Product, Banner

class CategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Category
        fields = [
            'category_name',
            'cat_image',
        ]

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            'brand_name',
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = {
            'product_name',
            'mrp',
            'offer',
            'quantity',
            'brand',
            'category',
            'image_1',
            'image_2',
            'image_3',
            'image_4',

        }

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = {
            'banner_title',
            'banner',
            'status',
        }

class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = {
            'poster_name',
            'poster',
            'status'
        }