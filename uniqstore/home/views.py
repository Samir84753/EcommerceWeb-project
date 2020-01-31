from django.shortcuts import render,redirect
from products.models import producttype,productitems,productreview
from accounts.models import cartitem
from . models import blog,blogcomment
from urllib.parse import urlencode
from django.urls import reverse
# Create your views here.
def indexview(request):
    products=productitems.objects.order_by('?')[:8]
    types=producttype.objects.all()

    context={
        'products':products,
        'types':types
    }
    return render(request,'index.html',context)

def aboutview(request):
    return render(request,'about.html')

def blogview(request):
    blogs=blog.objects.all()
    context={
        'blogs':blogs
    }
    return render(request,'blog.html',context)

def blogdetails(request):
    blogid=request.GET.get('bid')
    blogs=blog.objects.filter(id=blogid)
    latestblog = blog.objects.order_by('-postdate')
    comments=blogcomment.objects.filter(blogpostid=blogid).order_by('-commentdate')
    context={
        'blogs':blogs,
        'comments':comments,
        'latestblog':latestblog
    }
    return render(request,'blog-details.html',context)
def commentpost(request):
    user_ins=request.user
    blogid=request.POST.get('blogid')
    commentpost=request.POST.get('ucomment')
    commentsave=blogcomment(commenter=user_ins,comment=commentpost,blogpostid=blogid)
    commentsave.save()
     #for url redirect
    base_url = reverse('blogshow')
    query_string =  urlencode({'bid': blogid})
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url) 

    
def shopview(request):
    products=productitems.objects.order_by('?')
    types=producttype.objects.all()

    context={
        'products':products,
        'types':types
    }
    return render(request,'shop.html',context)

def contactview(request):
    return render(request,'contact.html')

def productdetailview(request):
    user_ins=request.user
    productid=request.GET.get('pid')
    productinfo=productitems.objects.filter(id=productid)
    reviews=productreview.objects.filter(reviewid=productid).order_by('-reviewdate')

    context={
        'productinfo':productinfo,
        'reviews':reviews
    }
    return render(request,'product-details.html',context)

def reviewsave(request):
    user_ins=request.user
    rid=request.POST.get('pid')
    reviewpost=request.POST.get('review')
    reviewsave=productreview(reviewer=user_ins,review=reviewpost,reviewid=rid)
    reviewsave.save()
    #for url redirect
    base_url = reverse('productdetail')
    query_string =  urlencode({'pid': rid})
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url) 
