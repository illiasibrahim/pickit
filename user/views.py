from django.http.response import FileResponse
from django.shortcuts import render,redirect, resolve_url
from vendor.models import Banner,Category,Poster,Product
from .models import Account
from django.contrib import messages,auth
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from twilio.rest import Client

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



def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        username = email.split('@')[0]
        
        if Account.objects.filter(email = email):
            messages.info(request,'This email address is already been used', extra_tags='email')
        elif Account.objects.filter(phone=phone):
            messages.info(request, 'This phone number is already been used',extra_tags='phone')
        else:
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['email'] = email
            request.session['phone'] = phone
            request.session['password'] = password
            request.session['username'] = username

            otp = random.randint(100000,999999)
            request.session['otp'] = otp
            print(otp)
            # account_sid = 'ACebf98e0fff644ccb36708cc0984af114'
            # auth_token = 'bbb861541cffc9f84cdbf8f47612d672'
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #                                 body= f'Your OTP for registration is -{ otp }',
            #                                 from_='+17816615925',
            #                                 to=f'+91{phone}'
            #                             )

            return redirect('verify-signup')

    return render(request,'user/register.html')


def sign_in(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = auth.authenticate(phone=phone, password=password)
        if user is not None:
            print('verified')
            auth.login(request, user)
            return redirect('/')
        else:
            print('no user')
            messages.info(request,'Invalid credentials')

    print('method get')
    return render(request,'user/signin.html')

def verify_signup(request):
    if request.method == 'POST':
        otp = str(request.session['otp'])
        entered_otp = str(request.POST['otp'])
        if otp == entered_otp:
            phone = request.session['phone']
            email = request.session['email']
            first_name = request.session['first_name']
            last_name = request.session['last_name']
            password = request.session['password']
            username = request.session['username']

            del request.session['otp']
            del request.session['phone']
            del request.session['email']
            del request.session['first_name']
            del request.session['last_name']
            del request.session['password']
            del request.session['username']

            user = Account.objects.create_user(phone=phone, email=email, first_name=first_name, last_name=last_name,password=password,username=username)
            user.save()
            return redirect('sign-in')
        else:
            messages.info(request,'The OTP you entered is wrong please try again',extra_tags='wrong otp')
    return render(request,'user/verify_otp.html')


@login_required(login_url='sign-in')
def logout(request):
    auth.logout(request)
    return redirect('/')

def product_detail(request,product_id):
    product = Product.objects.get(id= product_id)
    context = {
        'product' : product,
    }
    return render(request, 'user/product_detail.html',context)


