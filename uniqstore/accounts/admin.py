from django.contrib import admin
from . models import cartitem,carttotal,checkout,wishitems
# Register your models here.
class checkoutadmin(admin.ModelAdmin):
    list_display=('firstname','lastname','contactnumber','address','total')
admin.site.register(checkout,checkoutadmin)
admin.site.register(wishitems)