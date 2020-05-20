from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, ProductView, CheckoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>', ProductView.as_view(), name='product'),
    path('checkout', CheckoutView.as_view(), name='checkout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)