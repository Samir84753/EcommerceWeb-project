from django.contrib import admin
from . models import blog,blogcomment
# Register your models here.
class blogadmin(admin.ModelAdmin):
    list_display=('blogwriter','blogtitle','postdate')
admin.site.register(blog,blogadmin)
admin.site.register(blogcomment)