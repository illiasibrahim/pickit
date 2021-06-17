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
            'offer',
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
        self.fields['image_1'].widget.attrs['id'] = 'id_image_1'
        self.fields['image_2'].widget.attrs['id'] = 'id_image_2'
        self.fields['image_3'].widget.attrs['id'] = 'id_image_3'
        self.fields['image_4'].widget.attrs['id'] = 'id_image_4'
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
