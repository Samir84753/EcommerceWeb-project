from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from products.models import productitems
from accounts.models import cartitem,carttotal,checkout,wishitems
from django.contrib import messages
import yaml

# Create your views here.
def sign_in_upview(request):
    return render(request,'login-register.html')
def wishviewbasic(request):
    user_ins=request.user
    wishdetail=wishitems.objects.filter(wishuser=user_ins)
    context={
        'wishdetail':wishdetail,
    }

    return render(request,'wishlist.html',context)
def wishlistview(request):
    user_ins=request.user
    product_id=request.GET.get('pid')
    productname= productitems.objects.get(id=product_id).productname
    productprice= productitems.objects.get(id=product_id).productprice
    productstatus= productitems.objects.get(id=product_id).productstock
    wishadd= wishitems(wishuser = user_ins,productwish =productname,wishprice=productprice,wishstatus=productstatus,wishid=product_id)
    wishadd.save()
    return redirect('viewwish')

def deletewish(request,wishid):
    delwish=wishitems.objects.filter(wishid=wishid)
    delwish.delete()
    return redirect('viewwish')
def registeruser(request):
    username = request.POST.get('uname')
    email = request.POST.get('uemail')
    password = request.POST.get('upassword')
    re_password = request.POST.get('re_password')
    if User.objects.filter(email=email).exists():
        messages.error(request,"Email aready registered. Please use different email or login.")
        return redirect('Login_or_Register')
    if password==re_password:
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        try:
            sendemail('newregister.tpl',username,email)
        except:
            print("setup email and password in settings.py")
        user = authenticate(request,username=username, password=password)
        login(request,user)
        user_ins=request.user
        gtotals=0
        cartdototal=carttotal(cartuser=user_ins,gtotal=gtotals)
        cartdototal.save()
        
        return redirect('home')
    else:
        messages.error(request,"Passwords do not match.")
        return redirect('Login_or_Register')

def login_check(request):
    username=request.POST.get('lname')
    login_password=request.POST.get('lpass')
    user = authenticate(request,username=username, password=login_password)
    try:
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password do not match.")
            return redirect('Login_or_Register')
    except:
        return redirect('Login_or_Register')

    
def logout_task(request):
    logout(request)
    return redirect('home')

def cartviewbasic(request):
    user_ins=request.user
    cartdetail=cartitem.objects.filter(cartuser=user_ins)
    grtotal=carttotal.objects.get(cartuser=user_ins).gtotal
    context={
        'cartdetail':cartdetail,
        'grtotal':grtotal
    }
    return render(request,'cart.html',context)

def cartview(request):
    product_id=request.GET.get('pid')
    
    productname= productitems.objects.get(id=product_id).productname
    productprice= productitems.objects.get(id=product_id).productprice
    user_ins=request.user
    cartadd= cartitem(cartuser = user_ins,productcart =productname,cartprice=productprice)
    cartadd.save()
    #calculate total for confirmation
    gtotals=0
    cartusertotal=cartitem.objects.filter(cartuser=user_ins)
    for nums in cartusertotal:
        gtotals=gtotals+nums.subtotal
    cartdototal=carttotal.objects.get(cartuser=user_ins)
    cartdototal.gtotal=gtotals
    cartdototal.save()
    #..........
    return redirect('viewcart')

def updatecart(request):
    user_ins=request.user
    cartquantity=request.POST.get('productcartquantity')
    cartitemprice=request.POST.get('productcartprice')
    cartitemname=request.POST.get('productcartname')
    cartquantity=int(cartquantity)
    product_id=request.POST.get('cartid')
    updatecartquantity = cartitem.objects.get(id=product_id)
    updatecartquantity.quantity=cartquantity
    updatecartquantity.save()
     #calculate total for confirmation
    gtotals=0
    cartusertotal=cartitem.objects.filter(cartuser=user_ins)
    for nums in cartusertotal:
        gtotals=gtotals+nums.subtotal
    cartdototal=carttotal.objects.get(cartuser=user_ins)
    cartdototal.gtotal=gtotals
    cartdototal.save()
    #..........
    return redirect('viewcart')

def deletecart(request, cartitems_id):
    user_ins=request.user
     #update grandtotal
    priceofitem = cartitem.objects.get(id=cartitems_id).subtotal
    cartdototal=carttotal.objects.get(cartuser=user_ins)
    cartdototal.gtotal=cartdototal.gtotal-priceofitem
    cartdototal.save()
    #..........
    delcart = cartitem.objects.get(id=cartitems_id)
    delcart.delete()
    return redirect('viewcart')

def checkoutview(request):
    user_ins=request.user
    if checkout.objects.filter(checkoutuser=user_ins).exists():
        messages.error(request,"You already have a checkout pending. Please wait for your order to complete first.")
        return redirect('viewcart')
    else:
        #calculate total for confirmation
        gtotals=0
        cartusertotal=cartitem.objects.filter(cartuser=user_ins)
        for nums in cartusertotal:
            gtotals=gtotals+nums.subtotal
        cartdototal=carttotal.objects.get(cartuser=user_ins)
        cartdototal.gtotal=gtotals
        cartdototal.save()
        carttotaldetail=carttotal.objects.get(cartuser=user_ins).gtotal
        context={
            'carttotaldetail':carttotaldetail
        }
        return render(request,'checkout.html',context)

def docheckout(request):
    #user
    user_ins=request.user
    #user total
    carttotaldetail=carttotal.objects.get(cartuser=user_ins).gtotal
    #form data
    Firstname=request.POST.get('c_fname')
    Lastname=request.POST.get('c_lname')
    Email=request.POST.get('c_email')
    Contact=request.POST.get('c_contact')
    msg=request.POST.get('c_msg')
    Address=request.POST.get('c_address')
    #........................
    #cartdetail
    usercartitem=cartitem.objects.filter(cartuser=user_ins)
    products=[]
    quantity=[]
    userorderinfo={}
    for item in usercartitem:
        products.append(item.productcart)
        quantity.append(item.quantity)
    # print(products)
    # print(quantity)
    userorderinfo=dict(zip(products,quantity))
    # print(userorderinfo)

    checkoutsave = checkout(firstname = Firstname,lastname = Lastname,contactnumber = Contact,message=msg,address = Address,email = Email,total=carttotaldetail,checkoutuser=user_ins,orderinfo=userorderinfo)
    try:
        try:
            sendemail('checkoutdetail.tpl',user_ins,Email)
        except:
            print("setup email and password in settings.py")
        checkoutsave.save()
        delcart = cartitem.objects.filter(cartuser=user_ins)
        delcart.delete()
        #reset grandtotal
        cartdototal=carttotal.objects.get(cartuser=user_ins)
        cartdototal.gtotal=0
        cartdototal.save()
        #..........
        return redirect('viewcart')
    except:
        messages.error(request,"Invalid email")
        return redirect('viewcart')
    
    


def vieworders(request):
    try:
        user_ins=request.user
        order=checkout.objects.filter(checkoutuser=user_ins)
        usertotal=checkout.objects.get(checkoutuser=user_ins).total
        products=[]
        quantitys=[]
        for i in order:
            userorder=i.orderinfo
        userorder=yaml.load(userorder, Loader=yaml.FullLoader)
        userorder=sorted(userorder.items())
        return render(request,'myorders.html',{'userorder':userorder,'usertotal':usertotal})
    except:
        messages.error(request,"You don't have any orders.")
        return redirect('viewcart')

def sendemail(emailtemplate,username,toemail):
    from mail_templated import EmailMessage
    message = EmailMessage(emailtemplate, {'user': username},'your email',to=[toemail])
    message.send()