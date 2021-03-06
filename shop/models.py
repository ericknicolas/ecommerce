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

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])

class Order(models.Model):
    COUNTRIES = (
        ('US', 'us'),
        ('SPAIN', 'es'),
    )

    STATES = (
        ('California', 'ca'),
        ('Barcelona', 'bcn'),
    )

    first_name = models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=250)
    country = models.CharField(max_length=100, choices=COUNTRIES)
    state = models.CharField(max_length=100, choices=STATES)
    zipcode = models.CharField(max_length=100)
    items = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('order', args=[str(self.id)])
    
    

