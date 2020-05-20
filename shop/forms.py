from django import forms


class AddToCartForm(forms.Form):
    num_items = forms.IntegerField()
