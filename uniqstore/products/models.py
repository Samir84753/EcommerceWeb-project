from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class producttype(models.Model):
    category=models.CharField(max_length=100, blank=False)
    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Category'

    def __str__(self):
        return self.category


class productitems(models.Model):
    productname=models.CharField(max_length=100, blank=False)
    productprice=models.FloatField()
    productimg = models.ImageField(upload_to='product')
    productdescription=models.TextField(max_length=1500, blank=False)
    stockchoice =(('Available', 'Available'), ('Unavailable', 'Unavailable'))
    productstock=models.CharField(max_length=20,choices = stockchoice)
    categorytype = models.ForeignKey(producttype, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.productname
class productreview(models.Model):
    reviewid=models.IntegerField(default=1)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    review=models.TextField(max_length=1500, blank=False)
    reviewdate =models.DateTimeField("Date (mm/dd/yyyy)",auto_now_add=True,auto_now=False,blank=False,null=False)