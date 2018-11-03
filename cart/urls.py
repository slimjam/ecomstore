# from django.conf.urls.defaults import *
#
# urlpatterns = patterns(
#     'ecomstore.cart.views',
#     (r'^$', 'show_cart', { 'template_name': 'cart/cart.html' }, 'show_cart'), )
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.show_cart, name='show_cart'),
]
