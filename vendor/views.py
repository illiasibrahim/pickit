from typing import AsyncIterable, ContextManager, Tuple
from django.db.models.base import Model
from django.db.models.query import RawQuerySet
from django.http import request
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import activate
from vendor.models import Category, Brand, Product, Banner,Poster
from .forms import CategoryForm,BrandForm, CouponForm, PosterForm, ProductForm, BannerForm, EditProductForm
from .forms import EditCategoryForm
from user.models import Account, Coupon
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from math import ceil,floor, prod
from user.models import Order,OrderProduct,Payment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import datetime
from collections import Counter,OrderedDict
import random
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

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
        total_sale = 0
        to_sale = 0
        user_count = Account.objects.all().count()
        product_count = Product.objects.all().count()
        order_products = OrderProduct.objects.all().filter(ordered = True)
        todays_sales = OrderProduct.objects.filter(created_at__icontains=datetime.date.today(),ordered=True)
        for todays_sale in todays_sales:
            to_sale += int(todays_sale.quantity) * int(todays_sale.product_price)
        for order_product in order_products:
            total_sale += int(order_product.quantity)*int(order_product.product_price)
        
        # takes the data for sales per month graph
        m = datetime.date.today()
        sales_models = Order.objects.filter(is_ordered=True,created_at__month=m.month)
        sale = 0
        orders = Order.objects.all().filter(is_ordered=True, created_at__icontains=m.strftime("%Y-%m"))
        for order in orders:
            sale += int(order.total)
        sales = {m.strftime('%B'):sale}
        
        for i in range(10):
            try:
                m = m.replace(month=m.month-1,day=1)
            except ValueError:
                if m.month == 1:
                    m = m.replace(year=m.year-1,month=12,day=1)
                else:
                    # next month is too short to have "same date"
                    # pick your own heuristic, or re-raise the exception:
                    raise
            monthly_orders = Order.objects.all().filter(is_ordered=True, created_at__icontains=m.strftime("%Y-%m"))
            sale = 0
            for order in monthly_orders:
                sale += order.total
            sales[m.strftime('%B')] = sale

        res = OrderedDict(reversed(list(sales.items())))

        # takes the data for categorywise sales
        categories = Category.objects.all()

        category_dict = {}
        for category in categories:
            count = 0
            order_products = OrderProduct.objects.filter(product__category = category)
            for order_product in order_products:
                count += order_product.quantity

            category_dict[category.category_name]=count

        # takes the data for users per month
        today = datetime.date.today()
        users_count = Account.objects.filter(data_joined__month=today.month).count()
        users_dict = {today.strftime('%B'):users_count}
        for i in range(7):
            try:
                today = today.replace(month=today.month-1,day=1)
            except ValueError:
                if today.month == 1:
                    today = today.replace(year=today.year-1,month=12,day=1)
                else:
                    # next month is too short to have "same date"
                    # pick your own heuristic, or re-raise the exception:
                    raise
            monthly_users_count = Account.objects.filter(data_joined__month=today.month).count()
            users_dict[today.strftime('%B')] = monthly_users_count
        users_dict_ordered = OrderedDict(reversed(list(users_dict.items())))

        if request.is_ajax():

            color = 'rgba(53,135,164,0.7)'
            
            bar_color = []

            for s in range(len(category_dict)):
                r = random.randint(0,255)
                g = random.randint(0,255)
                b = random.randint(0,255)
                color = 'rgba({r},{g},{b},0.9)'.format(r=r,g=g,b=b)
                bar_color.append(color)

            sales_count = {
                'labels':list(res.keys()),
                'datasets' : [{
                    'label' : 'Sales per month',
                    'data' : list(res.values()),
                    'borderColor': None,
                    'backgroundColor': "#fbc658",
                }]
            }
            category_count = {
                'labels':list(category_dict.keys()),
                'datasets' : [{
                    'label' : 'Sales per month',
                    'data' : list(category_dict.values()),
                    'borderColor': "#51cbce",
                    'backgroundColor': bar_color,
                    "borderWidth":0,
                }]
            }
            users_count = {
                'labels':list(users_dict_ordered.keys()),
                'datasets' : [{
                    'label' : 'Sales per month',
                    'data' : list(users_dict_ordered.values()),
                    'borderColor': None,
                    'backgroundColor': "#51adae",
                }]
            }
            data_dict = {
                'sales_count' : sales_count,
                'category_count':category_count,
                'users_count':users_count,
            }
            return JsonResponse(data=data_dict,safe=False)
        
        context = {
            'user_count':user_count,
            'total_sale':total_sale,
            'product_count':product_count,
            'to_sale':to_sale,
        }
        return render(request,'vendor/dashboard.html',context)
    return redirect('admin-sign-in')


# views related to categories start from here

def category_view(request):
    if request.session.has_key('admin'):
        categories = Category.objects.all()
        paginator = Paginator(categories,10)
        page = request.GET.get('page')
        paged_categories = paginator.get_page(page)
        context = {
            'categories' : paged_categories,
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
            category_form = EditCategoryForm(request.POST,request.FILES, instance=category)
            if category_form.is_valid():
                category_form.save()
                return redirect('category')
        else:
            form = EditCategoryForm(instance=category)
        
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
        paginator = Paginator(brands,10)
        page = request.GET.get('page')
        paged_brands = paginator.get_page(page)
        context = {
            'brands' : paged_brands,
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
        paginator = Paginator(products,10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        context = {
            'products' : paged_products
        }
        return render(request,'vendor/product/product.html',context)
    return redirect('admin-sign-in')


def add_product(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
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
            product_form = EditProductForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product_form.save()
                return redirect('product')
        else:
            product_form = EditProductForm(instance=product)
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
        paginator = Paginator(banners,10)
        page = request.GET.get('page')
        paged_banners = paginator.get_page(page)
        context = {
            'banners' : paged_banners
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

def update_banner_status(request):
    if request.session.has_key('admin'):
        banner_id = request.GET['banner_id']
        banner = Banner.objects.get(id=banner_id)
        if banner.status:
            banner.status = False
            banner.save()
        else:
            banner.status = True
            banner.save()
        return JsonResponse({'status':True})
    return redirect('admin-sign-in')


def edit_banner(request, banner_id):
    if request.session.has_key('admin'):
        banner = Banner.objects.get(id = banner_id)
        if request.method == 'POST':
            banner_title = request.POST['banner-title']
            banner_image = request.POST['banner']
            return redirect('banner')
        context = {
            'banner' : banner,
        }
        return render(request, 'vendor/banner/edit_banner.html', context)
    return redirect('admin-sign-in')



# views related to banners start from here


def poster_view(request):
    if request.session.has_key('admin'):
        posters = Poster.objects.all()
        paginator = Paginator(posters,10)
        page = request.GET.get('page')
        paged_posters = paginator.get_page(page)
        context = {
            'posters': paged_posters
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


def update_poster_status(request):
    if request.session.has_key('admin'):
        poster_id = request.GET['poster_id']
        poster = Poster.objects.get(id=poster_id)
        if poster.status:
            poster.status = False
        else:
            poster.status = True
        poster.save()
        return JsonResponse({'status':True})
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
        paginator = Paginator(users,8)
        page = request.GET.get('page')
        paged_users = paginator.get_page(page)
        context = {
            'users' : paged_users
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


# global variables initialised for filtering by date
from_date = '2021-05-01 00:00:00.000000+05:30'
to_date =  datetime.date.today().strftime("%Y-%m-%d") + " 00:00:00.000000+05:30"

def order_view(request):
    if request.session.has_key('admin'):
        # this renders with the order.html file
        t_date = to_date[0:10]
        f_date = from_date[0:10]
        added_date = datetime.datetime.strptime(t_date, '%Y-%m-%d')
        added_date = added_date + datetime.timedelta(days=1)
        added_date = added_date.strftime("%Y-%m-%d") + " 00:00:00.000000+05:30"
        orders = Order.objects.filter(is_ordered=True, created_at__range=[from_date,added_date]).order_by('-created_at')
        paginator = Paginator(orders,10)
        page = request.GET.get('page')
        paged_orders = paginator.get_page(page)
        order_products = OrderProduct.objects.all()
        
        context ={
            'orders':paged_orders,
            'order_products':order_products,
            'f_date':f_date,
            't_date':t_date,
        }
        return render(request,'vendor/order.html',context)
    return redirect('admin-sign-in')


def approve(request):
    if request.session.has_key('admin'):
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.status = "Accepted"
        order.save()
        res = {
            'status':order.status,
        }
        return JsonResponse(res)
    return redirect('admin-sign-in')

def dispatch(request):
    if request.session.has_key('admin'):
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.status = "Dispatched"
        order.save()
        res = {
            'status' : order.status
        }
        return JsonResponse(res)
    return redirect('admin-sign-in')

def deliver(request):
    if request.session.has_key('admin'):
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.status = "Delivered"
        order.save()
        res = {
            'status' : order.status
        }
        return JsonResponse(res)
    return redirect('admin-sign-in')

def reject(request):
    if request.session.has_key('admin'):
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.status = "Rejected"
        order.save()
        res = {
            'status' : order.status
        }
        return JsonResponse(res)
    return redirect('admin-sign-in')

def filter_order(request):
    if request.session.has_key('admin'):
        global from_date
        global to_date
        from_d = request.GET['from_date']+ ' 00:00:00.000000+05:30'
        to_d = request.GET['to_date']+ ' 00:00:00.000000+05:30'
        from_date = from_d 
        to_date = to_d
        return JsonResponse({'status':True})
    return redirect('admin-sign-in')



def export(request):
    if request.session.has_key('admin'):
        from_d = request.GET['from_date']
        to_d = request.GET['to_date']
        file_type = request.GET['file_type']
        if from_d == "":
            from_d = '2021-05-01'
        if to_d == "":
            to_d = (datetime.date.today()+ datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        to_date = datetime.datetime.strptime(to_d, '%Y-%m-%d')
        to_date = to_date + datetime.timedelta(days=1)
        to_date = to_date.strftime("%Y-%m-%d") + " 00:00:00.000000+05:30"
        from_date = from_d + ' 00:00:00.000000+05:30'
        
        if Order.objects.filter(is_ordered = True,created_at__range=[from_date,to_date]).exists():
            if file_type == 'xls':
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename=Orders'+str(datetime.datetime.now())+'.xls'

                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Orders')
                row_number = 0
                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['Order Id', 'Customer','Order value', 'Order time','Status']

                for col_num in range(len(columns)):
                    ws.write(row_number, col_num, columns[col_num], font_style )

                font_style = xlwt.XFStyle()
                
                orders = Order.objects.filter(is_ordered = True,created_at__range=[from_date,to_date])

                rows = orders.values_list('order_number','user__first_name','total','created_at','status')

                for row in rows:
                    row_number += 1

                    for col_num in range(len(row)):
                        ws.write(row_number, col_num, str(row[col_num]), font_style )
                        col_num +=1
                    order_products = OrderProduct.objects.filter(order__order_number=row[0]).values_list('product__product_name','product__quantity','quantity')
                
                wb.save(response)
                return response
            elif file_type == 'pdf':
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'inline; attachment; filename=Orders'+str(datetime.datetime.now())+'.pdf'

                response['Content-Transfer-Encoding'] = 'binary'

                orders = Order.objects.filter(is_ordered = True,created_at__range=[from_date,to_date])
                order_products = OrderProduct.objects.all()

                html_string = render_to_string('vendor/pdf_output.html',{'orders':orders,'order_products':order_products,'from':from_d,'to':to_d})

                html = HTML(string=html_string)

                result = html.write_pdf()

                with tempfile.NamedTemporaryFile(delete=True) as output:
                    output.write(result)
                    output.flush()

                    output = open(output.name,'rb')
                    response.write(output.read())
                return response
        return redirect('order')
    return redirect('admin-sign-in')


def coupon_view(request):
    if request.session.has_key('admin'):
        coupons = Coupon.objects.all()
        categories = Category.objects.all()
        products = Product.objects.all().order_by('-offer')
        context = {
            'coupons':coupons,
            'categories':categories,
            'products':products,
        }
        return render(request,'vendor/coupon/coupon.html',context)
    return redirect('admin-sign-in')


def add_coupon(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            coupon_form = CouponForm(request.POST)
            if coupon_form.is_valid():
                coupon_form.save()
                return redirect('coupon')
        coupon_form = CouponForm()
        context = {
            'coupon_form':coupon_form,
        }
        return render(request,'vendor/coupon/add_coupon.html',context)
    return redirect('admin-sign-in')



def update_coupon_status(request):
    if request.session.has_key('admin'):
        coupon_id = request.GET['coupon_id']
        coupon = Coupon.objects.get(id=coupon_id)
        if coupon.status:
            coupon.status = False
        else:
            coupon.status = True
        coupon.save()
        return JsonResponse({'status':True,})
    return redirect('admin-sign-in')


def delete_coupon(request,coupon_id):
    if request.session.has_key('admin'):
        Coupon.objects.filter(id=coupon_id).delete()
        return redirect('coupon')
    return redirect('admin-sign-in')

def edit_coupon(request,coupon_id):
    if request.session.has_key('admin'):
        coupon = Coupon.objects.get(id = coupon_id)
        if request.method == 'POST':
            coupon_form = CouponForm(request.POST, request.FILES, instance=coupon)
            if coupon_form.is_valid():
                coupon_form.save()
                return redirect('coupon')
        else:
            coupon_form = CouponForm(instance=coupon)
        context = {
            'coupon' : coupon,
            'coupon_form' : coupon_form
        }
        return render(request, 'vendor/coupon/edit_coupon.html', context)
    return redirect('admin-sign-in')

def update_cat_offer(request):
    if request.session.has_key('admin'):
        cat_id = request.GET['cat_id']
        cat_offer = int(request.GET['cat_offer'])
        category = Category.objects.get(id=cat_id)
        category.cat_offer = cat_offer
        category.save()
        data = {
            'cat_offer':cat_offer,
        }
        return JsonResponse(data)
    return redirect('admin-sign-in')

def delete_cat_offer(request):
    if request.session.has_key('admin'):
        cat_id = request.GET['cat_id']
        category = Category.objects.get(id=cat_id)
        category.cat_offer = 0
        category.save()
        return JsonResponse({'staus':True})
    return redirect('admin-sign-in')


def update_product_offer(request):
    if request.session.has_key('admin'):
        product_id = request.GET['product_id']
        product_offer = request.GET['product_offer']
        product = Product.objects.get(id=product_id)
        product.offer = int(product_offer)
        product.save()
        data = {
            'product_offer':product_offer,
        }
        return JsonResponse(data)
    return redirect('admin-sign-in')