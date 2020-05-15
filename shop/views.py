from django.shortcuts import render
from django.views import generic

from .models import Products


class Home(generic.ListView):
    model = Products
    template_name = 'shop/home.html'


