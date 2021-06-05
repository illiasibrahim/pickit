from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('sign-in/',views.sign_in,name='sign-in'),
    path('sign-up/',views.sign_up,name='sign-up'),
    path('product/<product_id>/',views.product_detail, name='product'),
    
]