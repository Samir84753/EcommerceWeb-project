from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.indexview,name='home'),
    path('about',views.aboutview),
    path('blog',views.blogview,name='blog'),
    path('blog-details',views.blogdetails,name='blogshow'),
    path('shop',views.shopview),
    # path('home/shop',views.shopview),
    path('contact',views.contactview),
    path('productdetail',views.productdetailview),
    path('productdetail',views.productdetailview,name='productdetail'),
    path('postcomment',views.commentpost),
    # path('home/sendreview',views.reviewsave),
    path('sendreview',views.reviewsave),
    
]