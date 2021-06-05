from django.shortcuts import render
from vendor.models import Banner,Category,Poster,Product

# Create your views here.

def home(request):
    banners = Banner.objects.filter(status = True)
    categories = Category.objects.all()
    posters = Poster.objects.filter(status = True)
    products = Product.objects.all()
    context = {
        'banners' : banners,
        'categories' : categories,
        'posters' : posters,
        'products' : products,
    }
    return render(request,'user/index.html',context)

def sign_in(request):
    return render(request,'user/signin.html')

def sign_up(request):
    return render(request,'user/register.html')

def product_detail(request,product_id):
    product = Product.objects.get(id= product_id)
    context = {
        'product' : product,
    }
    return render(request, 'user/product_detail.html',context)