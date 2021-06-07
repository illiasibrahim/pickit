from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('sign-in/',views.sign_in,name='sign-in'),
    path('sign-up/',views.sign_up,name='sign-up'),
    path('verify-signup/',views.verify_signup,name='verify-signup'),
    path('logout/',views.logout,name='logout'),
    path('product/<product_id>/',views.product_detail, name='product'),
    
]