from django.shortcuts import render
from django.views import generic

from .models import Products


class Home(generic.ListView):
    model = Products
    template_name = 'shop/home.html'
    paginate_by = 8

    def get_queryset(self):
        try:
            query = self.request.GET.get('q')
        except:
            query = ''
        
        if(query != '' and query is not None):
            object_list = Products.objects.filter(title__icontains = query)
        else:
            object_list = Products.objects.all()

        return object_list
