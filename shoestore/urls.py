from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:category_slug>/<str:slug>', views.prod_details, name='details'),
    # path('add-to-cart/<str:slug>/<str:color>/', views.add_to_cart, name="add"),
    path('add-to-cart/<str:slug>/', views.add_to_cart, name="add"),
    path('cart/', views.cart_view, name="cart"),
    path('remove/<str:slug>/', views.remove_from_cart, name="remove"),
    path('increase/<str:slug>/', views.increase_cart, name="increase"),
    path('decrease/<str:slug>/', views.decrease_cart, name="decrease"),
    path('<str:postslug>', views.allprod_by_category, name='allcatpost'),
        #User Authentication urls
    path('userlogin/', views.login, name='userlogin'),
    path('usersignup/', views.signup, name='usersignup'),
    path('userlogout/', views.logout, name='logout'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    