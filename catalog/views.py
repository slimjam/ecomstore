from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from django.urls import reverse
from cart import cart
from django.http import HttpResponseRedirect
from .forms import ProductAddToCartForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from ecomstore.settings import PRODUCTS_PER_PAGE


def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # need to evaluate the HTTP method
    if request.method == 'POST':    # add to cart…create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        if form.is_valid():           # check if posted data is valid
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            if request.session.test_cookie_worked():      # if test cookie worked, get rid of it
                request.session.delete_test_cookie()
                return HttpResponseRedirect(reverse('show_cart'))
    else:   # it’s a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    form.fields['product_slug'].widget.attrs['value'] = product_slug          # assign the hidden input the product slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    return render(request, 'catalog/product.html', context=locals())


def index(request, template_name="catalog/index.html"):
    page_title = 'Online shop'
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Checkout':
            cart_items = cart.get_cart_items(request)
            for cart_item in cart_items:
                p = cart_item.product
                p.quantity -= cart_item.quantity
                p.save()
            cart.remove_from_cart(request, cart_items)
            message = f"""
            Thank you, for buying something in our shop.
            If you wanna , you can continue.
            Pleasure work for you.
            """
    return render(request, template_name, context=locals())


def show_category(request, category_slug, template_name="catalog/category.html"):
    q = request.GET.get('q', '')
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all().order_by('-is_bestseller')
    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        results = paginator.page(1).object_list
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, template_name, context=locals())
