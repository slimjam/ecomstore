from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from django.urls import reverse
from cart import cart
from django.http import HttpResponseRedirect
from .forms import ProductAddToCartForm


# new product view, with POST vs GET detection
def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.all()
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # need to evaluate the HTTP method
    print(request.method)
    if request.method == 'POST':    # add to cart…create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        if form.is_valid():           # check if posted data is valid
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # return HttpResponseRedirect(reverse('show_cart'))
            if request.session.test_cookie_worked():      # if test cookie worked, get rid of it
                request.session.delete_test_cookie()
                return HttpResponseRedirect(reverse('show_cart'))
    else:   # it’s a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=':')
    form.fields['product_slug'].widget.attrs['value'] = product_slug          # assign the hidden input the product slug
    # set the test cookie on our first GET request
    # TODO найти разницу между колвом и проверять не больше ли чем есть на складе, а изменять значение в бд только после кнопки купить
    request.session.set_test_cookie()
    return render(request, 'catalog/product.html', context=locals())


def index(request, template_name="catalog/index.html"):
    page_title = 'Online shop'
    # return render_to_response(template_name, context=locals())
    return render(request, template_name, context=locals())

# rewrite by normal way using dict no locals()
# and input arg to func should be only request


def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, template_name, context=locals())


# def show_product(request, product_slug, template_name="catalog/product.html"):
#     p = get_object_or_404(Product, slug=product_slug)
#     categories = p.categories.filter(is_active=True)
#     page_title = p.name
#     meta_keywords = p.meta_keywords
#     meta_description = p.meta_description
#     return render(request, template_name, context=locals())

# TODO поубирать все не нужное, добавить гэт для карты, если проходит валидацию поздравлять с покупкой и очищать карту, сделать пагинацию и сделать опшионс