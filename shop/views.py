from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from .models import Products
from .forms import AddToCartForm
from .filters import ItemFilter


class HomeView(FilterView, ListView):
    model = Products
    template_name = 'shop/home.html'
    filterset_class = ItemFilter
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = list(set([product.category for product in Products.objects.all()]))

        return context


class ProductView(FormMixin, DetailView):
    model = Products
    form_class = AddToCartForm
    template_name = 'shop/product.html'
    context_object_name = 'product'
    success_url = reverse_lazy('home')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        cart_items = self.request.session.get('cart', {})

        if(str(self.object.id) in cart_items):
            cart_items[str(self.object.id)] += form.cleaned_data['num_items']
        else:
            cart_items[str(self.object.id)] = form.cleaned_data['num_items']

        self.request.session['cart'] = cart_items

        return super().form_valid(form)


class CheckoutView(ListView):
    model = Products
    template_name = 'shop/checkout.html'

