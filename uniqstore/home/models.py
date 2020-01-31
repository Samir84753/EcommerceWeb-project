from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class blog(models.Model):
    blogwriter=models.ForeignKey(User,on_delete=models.CASCADE)
    blogtitle=models.CharField(max_length=200, blank=False)
    blogbody=models.TextField(max_length=1500, blank=False)
    img = models.ImageField(upload_to='imgblog')
    postdate =models.DateTimeField("Date (mm/dd/yyyy)",auto_now_add=True,auto_now=False,blank=False,null=False)

    class Meta:
        verbose_name = 'Blog Section'
        verbose_name_plural = 'Blog Section'
class blogcomment(models.Model):
    blogpostid=models.IntegerField(default=1)
    commenter=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField(max_length=1500, blank=False)
    commentdate =models.DateTimeField("Date (mm/dd/yyyy)",auto_now_add=True,auto_now=False,blank=False,null=False)
