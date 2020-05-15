from django.db import models
from django.urls import reverse


class Products(models.Model):
    title = models.CharField(max_length=200, help_text='Introduce product title')
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=50)
    description = models.TextField(help_text='Introduce a brief description for the product')
    image = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse('product-detail', args=[str(self.id)])

