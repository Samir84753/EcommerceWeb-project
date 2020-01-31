from django.db import models
from products.models import productitems
from django.contrib.auth.models import User
from datetime import datetime
from products.models import productitems


class cartitem(models.Model):
    productcart=models.CharField(max_length=200,default='')
    quantity=models.IntegerField(default=1)
    cartprice=models.FloatField(blank=True)
    cartuser=models.ForeignKey(User,on_delete=models.CASCADE)
    subtotal=models.FloatField(blank=True,default=cartprice)
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Item'
    def save(self, *args, **kwargs):
        self.subtotal=self.cartprice*self.quantity
        super().save(*args, **kwargs)
        
class carttotal(models.Model):
    cartuser=models.ForeignKey(User,on_delete=models.CASCADE)
    gtotal=models.FloatField(blank=True,default=0)

class checkout(models.Model):
    firstname=models.CharField(max_length=100, blank=False)
    lastname=models.CharField(max_length=100, blank=False)
    contactnumber=models.CharField(max_length=10, blank=False)
    message=models.TextField(max_length=1500, blank=True)
    address=models.CharField(max_length=100, blank=False)
    email=models.EmailField(max_length=250, blank=False)
    total=models.FloatField(blank=True,default=0)
    checkoutuser=models.ForeignKey(User,on_delete=models.CASCADE)
    orderinfo=models.TextField(max_length=1000,blank=True,default='')
    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkout List'

class wishitems(models.Model):
    productwish=models.CharField(max_length=200,default='')
    wishprice=models.FloatField(blank=True)
    wishuser=models.ForeignKey(User,on_delete=models.CASCADE)
    wishstatus=models.CharField(max_length=200,default='')
    wishid=models.IntegerField(blank=False,default=0)
    class Meta:
        verbose_name = 'Wish List'
        verbose_name_plural = 'Wish List'
