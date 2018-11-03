from django.shortcuts import render
from cart import cart
# from django.views.decorators.csrf import csrf_protect
#
#
# @csrf_protect
def show_cart(request, template_name="cart/cart.html"):
    print(request.method)
    if request.method == 'POST':
        postdata = request.POST.copy()
        print(postdata)
        for p in postdata:
            print(postdata)
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render(request, template_name, locals())
    # else:
    #     return render(request, template_name, {})
