from django import forms
from .models import Product
from django.core import validators


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

        def clean_price(self):
            if self.cleaned_data['price'] <= 0:
                raise forms.ValidationError('Price must be greater than zero.')
            return self.cleaned_data['price']


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'size': '2',
                'value': '1',
                'class': 'quantity',
                'maxlength': '5'
            }
        ),
        error_messages={'invalid': 'Please enter a valid quantity.'},
        min_value=1
    )
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        product_slug = self.data.get('product_slug', '')
        products = Product.objects.filter(slug=product_slug)
        for pr in products:
            q = self.data.get('quantity', '')
            try:
                if int(q) > pr.quantity:
                    raise forms.ValidationError("Sorry, you choose more than available products.")
            except ValueError:
                pass
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data
