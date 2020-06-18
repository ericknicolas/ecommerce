from django import forms
from .models import Order


class AddToCartForm(forms.Form):
    num_items = forms.IntegerField()

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address','country','state','zipcode']
        widgets = {
            'country': forms.Select(attrs={'class': 'custom-select d-block w-100'}),
            'state': forms.Select(attrs={'class': 'custom-select d-block w-100'})
        }



