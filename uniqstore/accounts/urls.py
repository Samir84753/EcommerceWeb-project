from django.urls import path,include
from . import views
urlpatterns = [
    path('signup_or_signin',views.sign_in_upview,name='Login_or_Register'),
    path('home/registration',views.registeruser),
    path('home/login',views.login_check),

    path('logout',views.logout_task),
    # path('home/logout',views.logout_task),

    path('wishlist',views.wishlistview),
    path('cart',views.cartview),
    path('viewcart',views.cartviewbasic,name='viewcart'),
    # path('home/viewcart',views.cartviewbasic),
    path('update',views.updatecart),
    path("delete/<int:cartitems_id>/", views.deletecart),
    path("deletewish/<int:wishid>/", views.deletewish),
    # path('grandtotal',views.dototal),
    path('checkoutview',views.checkoutview),
    path('checkout',views.docheckout),

    path('myorder',views.vieworders),
    # path('home/myorder',views.vieworders),
    
    path('viewwish',views.wishviewbasic,name='viewwish')
]


