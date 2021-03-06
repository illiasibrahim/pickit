from user.models import Coupon
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
    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)
        self.fields['category_name'].widget.attrs['required'] = 'required'
        self.fields['cat_image'].widget.attrs['id'] = 'id_image'
        self.fields['cat_image'].widget.attrs['required'] = 'required'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class EditCategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Category
        fields = [
            'category_name',
            'cat_image',
        ]
    def __init__(self,*args,**kwargs):
        super(EditCategoryForm,self).__init__(*args,**kwargs)
        self.fields['category_name'].widget.attrs['required'] = 'required'
        self.fields['cat_image'].widget.attrs['id'] = 'id_image'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            'brand_name',
        ]
    def __init__(self,*args,**kwargs):
        super(BrandForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class ProductForm(forms.ModelForm):
    image_1 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image_2 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image_3 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image_4 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = {
            'product_name',
            'mrp',
            'quantity',
            'brand',
            'category',
            'description',
            'image_1',
            'image_2',
            'image_3',
            'image_4',
        }

    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)
        self.fields['mrp'].widget.attrs['name']='mrp'
        self.fields['image_1'].widget.attrs['id'] = 'id_image_1'
        self.fields['image_2'].widget.attrs['id'] = 'id_image_2'
        self.fields['image_3'].widget.attrs['id'] = 'id_image_3'
        self.fields['image_4'].widget.attrs['id'] = 'id_image_4'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].widget.attrs['required'] = 'required'

class EditProductForm(forms.ModelForm):
    image_1 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image_2 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image_3 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    image_4 = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = {
            'product_name',
            'mrp',
            'quantity',
            'brand',
            'category',
            'description',
            'image_1',
            'image_2',
            'image_3',
            'image_4',
        }

    def __init__(self,*args,**kwargs):
        super(EditProductForm,self).__init__(*args,**kwargs)
        self.fields['mrp'].widget.attrs['name']='mrp'
        self.fields['image_1'].widget.attrs['id'] = 'id_image_1'
        self.fields['image_2'].widget.attrs['id'] = 'id_image_2'
        self.fields['image_3'].widget.attrs['id'] = 'id_image_3'
        self.fields['image_4'].widget.attrs['id'] = 'id_image_4'
        self.fields['product_name'].widget.attrs['required'] = 'required'
        self.fields['mrp'].widget.attrs['required'] = 'required'
        self.fields['quantity'].widget.attrs['required'] = 'required'
        self.fields['brand'].widget.attrs['required'] = 'required'
        self.fields['category'].widget.attrs['required'] = 'required'
        self.fields['description'].widget.attrs['required'] = 'required'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'




class BannerForm(forms.ModelForm):
    banner = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Banner
        fields = {
            'banner_title',
            'banner',
            'status',
        }

    def __init__(self,*args,**kwargs):
        super(BannerForm,self).__init__(*args,**kwargs)
        self.fields['banner_title'].widget.attrs['required'] = 'required'
        self.fields['banner'].widget.attrs['required'] = 'required'
        self.fields['banner'].widget.attrs['id'] = 'id_image'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

class PosterForm(forms.ModelForm):
    poster = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Poster
        fields = {
            'poster_name',
            'poster',
            'status'
        }

    def __init__(self,*args,**kwargs):
        super(PosterForm,self).__init__(*args,**kwargs)
        self.fields['poster_name'].widget.attrs['required'] = 'required'
        self.fields['poster'].widget.attrs['id'] = 'id_image'
        self.fields['poster'].widget.attrs['required'] = 'required'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = {
            'code',
            'discount',
            'status',
        }
    def __init__(self,*args,**kwargs):
        super(CouponForm,self).__init__(*args,**kwargs)
        self.fields['code'].widget.attrs['required'] = 'required'
        self.fields['discount'].widget.attrs['required'] = 'required'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'