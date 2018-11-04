from django import template
from cart import cart
from catalog.models import Category
from django.contrib.flatpages.models import FlatPage
from urllib.parse import urlencode

register = template.Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count}


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.objects.filter(is_active=True)
    return {
        'active_categories': active_categories,
        'request_path': request_path
    }


@register.inclusion_tag("tags/footer.html")
def footer_links():
    flatpage_list = FlatPage.objects.all()
    return {'flatpage_list': flatpage_list}


@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator):
    raw_params = request.GET.copy()
    page = raw_params.get('page', 1)
    p = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urlencode(raw_params)
    return {
        'request': request,
        'paginator': paginator,
        'p': p,
        'params': params
    }
