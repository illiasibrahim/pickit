from typing import AsyncIterable, ContextManager
from django.http import request
from django.shortcuts import redirect, render
from django.utils.translation import activate
from vendor.models import Category, Brand, Product, Banner,Poster
from .forms import CategoryForm,BrandForm, PosterForm, ProductForm, BannerForm
from user.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required


# Create your views here.

def sign_in(request):
    if request.session.has_key('admin'):
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            password = request.POST['password']
            user = auth.authenticate(phone=phone, password=password)
            if user is not None:
                print(user.phone)
                if user.is_superadmin:
                    print('usr is not superuser')
                    request.session['admin'] = phone
                    return redirect('dashboard')
                else:
                    print('user is not super user')
                    messages.info(request,'Invalid login credentials')
            else:
                print('user is none')
                messages.info(request, 'Invalid login credentials')
        return render(request,'vendor/signin.html')


def logout(request):
    if request.session.has_key('admin'):
        del request.session['admin']
    return redirect('admin-sign-in')





def dashboard(request):
    if request.session.has_key('admin'):
        return render(request,'vendor/dashboard.html')
    return redirect('admin-sign-in')


# views related to categories start from here

def category_view(request):
    if request.session.has_key('admin'):
        categories = Category.objects.all()
        context = {
            'categories' : categories,
        }
        return render(request,'vendor/category/category.html',context)
    return redirect('admin-sign-in')


def add_category(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('category')
            else:
                print('invalid form')
        else:
            
            category_form = CategoryForm()
            context = {
            'category_form'  : category_form,
            }
            return render(request,'vendor/category/add_category.html',context)
    return redirect('admin-sign-in')



def delete_category(request,category_id):
    if request.session.has_key('admin'):
        Category.objects.filter(id=category_id).delete()
        return redirect('category')
    return redirect('admin-sign-in')



def edit_category(request,category_id):
    if request.session.has_key('admin'):
        category = Category.objects.get(id=category_id)
        if request.method == 'POST':
            category_form = CategoryForm(request.POST,request.FILES, instance=category)
            if category_form.is_valid():
                category_form.save()
                return redirect('category')
        else:
            form = CategoryForm(instance=category)
        
        context ={
            'form' : form,
            'category' : category
        }
        return render(request,'vendor/category/edit_category.html',context)
    return redirect('admin-sign-in')


# views related to brands start from here


def brand_view(request):
    if request.session.has_key('admin'):
        brands = Brand.objects.all()
        context = {
            'brands' : brands,
        }
        return render(request, 'vendor/brand/brand.html',context)
    return redirect('admin-sign-in')



def add_brand(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            brand_form = BrandForm(request.POST)
            if brand_form.is_valid():
                brand_form.save()
                return redirect('brand')
        else:
            brand_form = BrandForm()
            context = {
                'brand_form' : brand_form,
            }
            return render(request, 'vendor/brand/add_brand.html',context)
    return redirect('admin-sign-in')
    

def edit_brand(request,brand_id):
    if request.session.has_key('admin'):
        brand = Brand.objects.get(id=brand_id)
        if request.method == 'POST':
            brand_form = BrandForm(request.POST, instance=brand)
            if brand_form.is_valid():
                brand_form.save()
                return redirect('brand')
        else:
            brand_form = BrandForm(instance=brand)
        context = {
            'brand_form' : brand_form,
        }
        return render(request,'vendor/brand/edit_brand.html',context)
    return redirect('admin-sign-in')



def delete_brand(request, brand_id):
    if request.session.has_key('admin'):
        Brand.objects.filter(id=brand_id).delete()
        return redirect('brand')
    else:
        return redirect('admin-sign-in')



# views related to products start from here


def product_view(request):
    if request.session.has_key('admin'):
        products = Product.objects.all()
        context = {
            'products' : products
        }
        return render(request,'vendor/product/product.html',context)
    return redirect('admin-sign-in')


def add_product(request):
    if request.session.has['key']:
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                mrp = product_form.cleaned_data.get("mrp")
                offer = product_form.cleaned_data.get("offer")
                discount = mrp * (offer/100)
                discount_price = mrp - discount
                product = Product.objects.get(offer = offer)
                product.discount = discount
                product.discount_price = discount_price
                product.save()
                return redirect('product')
        else:
            product_form = ProductForm()
        context = {
            'product_form' : product_form
        }
        return render(request,'vendor/product/add_product.html', context)
    return redirect('admin-sign-in')



def delete_product(request,product_id):
    if request.session.has_key('admin'):
        Product.objects.filter(id=product_id).delete()
        return redirect('product')
    return redirect('admin-sign-in')



def edit_product(request,product_id):
    if request.session.has_key('admin'):
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product_form.save()
                mrp = product_form.cleaned_data.get("mrp")
                offer = product_form.cleaned_data.get("offer")
                discount = mrp * (offer/100)
                discount_price = mrp - discount
                product.discount = discount
                product.discount_price = discount_price
                product.save()
                return redirect('product')
        else:
            product_form = ProductForm(instance=product)
        context = {
            'product' : product,
            'product_form' : product_form,
        }
        return render(request, 'vendor/product/edit_product.html',context)
    return redirect('admin-sign-in')



# views related to banners start from here

def banner_view(request):
    if request.session.has_key('admin'):
        banners = Banner.objects.all()
        context = {
            'banners' : banners
        }
        return render(request, 'vendor/banner/banner.html', context)
    return redirect('admin-sign-in')


def add_banner(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            banner_form = BannerForm(request.POST, request.FILES)
            if banner_form.is_valid():
                banner_form.save()
                return redirect('banner')
        else:
            banner_form = BannerForm()
            context = {
                'banner_form' : banner_form

            }
        return render(request, 'vendor/banner/add_banner.html', context)
    return redirect('admin-sign-in')



def delete_banner(request, banner_id):
    if request.session.has_key('admin'):
        Banner.objects.filter(id = banner_id).delete()
        return redirect('banner')
    return redirect('admin-sign-in')



def edit_banner(request, banner_id):
    if request.session.has_key('admin'):
        banner = Banner.objects.get(id = banner_id)
        if request.method == 'POST':
            banner_form = BannerForm(request.POST, request.FILES, instance=banner)
            if banner_form.is_valid():
                banner_form.save()
                return redirect('banner')
        else:
            banner_form = BannerForm(instance=banner)
        context = {
            'banner' : banner,
            'banner_form' : banner_form
        }
        return render(request, 'vendor/banner/edit_banner.html', context)
    return redirect('admin-sign-in')



# views related to banners start from here


def poster_view(request):
    if request.session.has_key('admin'):
        posters = Poster.objects.all()
        context = {
            'posters': posters
        }
        return render(request, 'vendor/poster/poster.html', context)
    return redirect('admin-sign-in')


def add_poster(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            poster_form = PosterForm(request.POST, request.FILES)
            if poster_form.is_valid():
                poster_form.save()
                return redirect('poster')
        else:
            poster_form = PosterForm()
        context = {
            'poster_form' : poster_form,
        }
        return render(request, 'vendor/poster/add_poster.html', context)
    return redirect('admin-sign-in')



def delete_poster(request,poster_id):
    if request.session.has_key('admin'):
        Poster.objects.filter(id= poster_id).delete()
        return redirect('poster')
    return redirect('admin-sign-in')



def edit_poster(request, poster_id):
    if request.session.has_key('admin'):
        poster = Poster.objects.get(id= poster_id)
        if request.method == 'POST':
            poster_form = PosterForm(request.POST,request.FILES,instance=poster)
            if poster_form.is_valid():
                poster_form.save()
                return redirect('poster')
        else:
            poster_form = PosterForm(instance=poster)
            context = {
                'poster_form' : poster_form,
                'poster' : poster
            }
        return render(request, 'vendor/poster/edit_poster.html',context)
    return redirect('admin-sign-in')


# views related to users starts from here 


def user_view(request):
    if request.session.has_key('admin'):
        users = Account.objects.all()
        context = {
            'users' : users
        }
        return render(request, 'vendor/user.html',context)
    return redirect('admin-sign-in')


def delete_user(request,user_id):
    if request.session.has_key('admin'):
        Account.objects.filter(id = user_id).delete()
        return redirect('user')
    return redirect('admin-sign-in')


def block_user(request,user_id):
    if request.session.has_key('admin'):
        user = Account.objects.get(id=user_id)
        user.has_access = False
        user.save()
        return redirect('user')
    return redirect('admin-sign-in')


def unblock_user(request, user_id):
    if request.session.has_key('admin'):
        user = Account.objects.get(id=user_id)
        user.has_access = True
        user.save()
        return redirect('user')
    return redirect('admin-sign-in')

