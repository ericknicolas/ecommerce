from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from .models import Products
from .forms import AddToCartForm, CheckoutForm
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


class CheckoutView(FormMixin, ListView):
    model = Products
    template_name = 'shop/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('home')

    def get_queryset(self):
        cart_items = self.request.session.get('cart', {})
        
        return Products.objects.filter(id__in = cart_items)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cart_items = self.request.session.get('cart', {})
        total = 0

        for product in data['object_list']:
            if (str(product.id)) in cart_items:
                total += product.discount_price * cart_items[str(product.id)]

        data['total'] = total

        return data
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object_list = self.get_queryset()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        order = form.save(commit=False)
        order.items = self.request.session.get('cart', {})
        order.save()

        self.request.session.flush()

        return super().form_valid(form)



