from typing import AsyncIterable, ContextManager
from django.shortcuts import redirect, render
from django.utils.translation import activate
from vendor.models import Category, Brand, Product, Banner,Poster
from .forms import CategoryForm,BrandForm, PosterForm, ProductForm, BannerForm

# Create your views here.

def sign_in(request):
    return render(request,'vendor/signin.html')

def dashboard(request):
    return render(request,'vendor/dashboard.html')


# views related to categories start from here

def category_view(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request,'vendor/category/category.html',context)

def add_category(request):
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

def delete_category(request,category_id):
    Category.objects.filter(id=category_id).delete()
    return redirect('category')

def edit_category(request,category_id):
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


# views related to brands start from here

def brand_view(request):
    brands = Brand.objects.all()
    context = {
        'brands' : brands,
    }
    return render(request, 'vendor/brand/brand.html',context)

def add_brand(request):
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
    

def edit_brand(request,brand_id):
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



def delete_brand(request, brand_id):
    Brand.objects.filter(id=brand_id).delete()
    return redirect('brand')



# views related to products start from here


def product_view(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request,'vendor/product/product.html',context)

def add_product(request):
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

def delete_product(request,product_id):
    Product.objects.filter(id=product_id).delete()
    return redirect('product')

def edit_product(request,product_id):
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



# views related to banners start from here

def banner_view(request):
    banners = Banner.objects.all()
    context = {
        'banners' : banners
    }
    return render(request, 'vendor/banner/banner.html', context)

def add_banner(request):
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

def delete_banner(request, banner_id):
    Banner.objects.filter(id = banner_id).delete()
    return redirect('banner')

def edit_banner(request, banner_id):
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


# views related to banners start from here

def poster_view(request):
    posters = Poster.objects.all()
    context = {
        'posters': posters
    }
    return render(request, 'vendor/poster/poster.html', context)

def add_poster(request):
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

def delete_poster(request,poster_id):
    Poster.objects.filter(id= poster_id).delete()
    return redirect('poster')
    
def edit_poster(request, poster_id):
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


# views related to users starts from here 

def user_view(request):
    return render(request, 'vendor/user.html')