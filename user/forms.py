from django import forms
from django.db import models
from django.db.models import fields
from .models import DeliveryAddress, Profile,ReviewRating

class AddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = {
            'first_name',
            'last_name',
            'phone',
            'email',
            'country',
            'state',
            'street',
            'city',
            'pin',
            'building',
            'landmark',
        }

    def __init__(self,*args,**kwargs):
        super(AddressForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter the first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter the first name'
        self.fields['phone'].widget.attrs['placeholder'] = '+91 00000 00000'
        self.fields['email'].widget.attrs['placeholder'] = 'example@mail.com'
        self.fields['state'].widget.attrs['placeholder'] = 'state'
        self.fields['street'].widget.attrs['placeholder'] = 'wall street 09'
        self.fields['city'].widget.attrs['placeholder'] = 'hilite city'
        self.fields['pin'].widget.attrs['placeholder'] = '000 000'
        self.fields['building'].widget.attrs['placeholder'] = ''
        self.fields['landmark'].widget.attrs['placeholder'] = "near st.sebastian's church"
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class ProfileForm(forms.ModelForm):
    display_picture = forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = {
            'display_picture'
        }
    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['display_picture'].widget.attrs['class'] = 'form-control'
        self.fields['display_picture'].widget.attrs['required'] = 'required'
        self.fields['display_picture'].widget.attrs['id'] = 'id_image'
 

class ReviewRatingForm(forms.ModelForm):
     class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']