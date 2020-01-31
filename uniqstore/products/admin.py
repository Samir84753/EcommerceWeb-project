from django.contrib import admin
from . models import producttype,productitems,productreview
# Register your models here.
admin.site.register(producttype)
admin.site.register(productitems)
admin.site.register(productreview)