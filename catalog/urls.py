from django.urls import path, re_path
# from django.conf.urls.defaults import *
from . import views
# urlpatterns = patterns(
#     'ecomstore.catalog.views',
#     (r'^$', 'index',
#      {'template_name': 'catalog/index.html'},
#      'catalog_home'),
#     (r'^category/(?P<category_slug>[-\w]+)/$',
#      'show_category',
#      {'template_name': 'catalog/category.html'},
#      'catalog_category'),
#     (r'^product/(?P<product_slug>[-\w]+)/$',
#      'show_product',
#      {'template_name': 'catalog/product.html'},
#      'catalog_product'),
# )
urlpatterns = [
    re_path(r'^$', views.index, name='catalog_home'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.show_category, name='catalog_category'),
    re_path(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product, name='catalog_product'),
]
