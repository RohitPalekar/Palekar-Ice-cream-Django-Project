from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from iceapp.models import IcecreamInfo, Cart, Order, OrderHistory,UserInfo,FranchiseQuery,UserInfo
from django.db.models import Q
import razorpay
from django.utils.timezone import now
from django.core.mail import send_mail
import re
from django.utils.timezone import now


# Create your views here.
def index(request):
    return render(request, 'index.html')

def ourstory(request):
    return render(request,'ourstory.html')

def locations(request):
    return render(request,'locations.html')

def franchisequeries(request):
    if request.method == 'GET':
        return render(request,'franchisequeries.html')
    else:
        print("post method")
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        print("State: ",state)
        fq = FranchiseQuery.objects.create(name=name,email=email,phone=phone,street=street,city=city,state=state,pincode=pincode)
        fq.save()
        context ={}
        context['success'] = "Query Submitted Successfully..!!!"
        return render(request,'franchisequeries.html',context)

def user_login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        un = request.POST['username']
        p = request.POST['password']
        print(un,p)
        u=authenticate(username=un,password=p)
        print(u)
        context ={}
        if u==None:
            context['errmsg'] = 'Invalid Credentials'
            return render(request,'login.html',context)
        else:
            login(request,u)       
            return redirect('/index')

def user_logout(request):
    logout(request)
    return redirect('/index')

def signup(request):
    context = {}
    
    if request.method == 'GET':        
        return render(request, 'signup.html')
    else:
        fn = request.POST['fname']    
        ln = request.POST['lname']    
        un = request.POST['username']    
        e = request.POST['email']    
        con = request.POST['contact']    
        p = request.POST['password']    
        cp = request.POST['cpassword']    
        add = request.POST['address']

        # Validation checks
        if not all([fn, ln, un, e, p, cp, con, add]):
            context['errmsg'] = "Please fill out all fields"
        elif User.objects.filter(username=un).exists():
            context['errmsg'] = "User Already exists..!!"
        elif p != cp:
            context['errmsg'] = "Password and confirm password do not match"
        elif len(p) < 8:
            context['errmsg'] = "Password length must be at least 8 characters"
        elif not fn.isalpha():
            context['errmsg'] = "First name cannot contain numbers or special characters"
        elif not ln.isalpha():
            context['errmsg'] = "Last name cannot contain numbers or special characters"
        elif not re.match(r'^\d{10}$', con):
            context['errmsg'] = "Contact number must be exactly 10 digits"
        elif con == "0000000000":
            context['errmsg'] = "Contact number cannot be all zeros"
        
        else:
            # Save the user if all validations pass
            u = User.objects.create(username=un, first_name=fn, last_name=ln, email=e)
            u.set_password(p)
            u.save()

            # Save additional user information
            UserInfo.objects.create(uid=u, mobile=con, address=add)
            
            context['success'] = "User created successfully!"
    
    return render(request, 'signup.html', context)

def ordernow(request,iid):
    if request.user.is_authenticated:        
        u = User.objects.filter(id=request.user.id)
        i = IcecreamInfo.objects.filter(id=iid)
        q1=Q(uid=u[0])
        q2=Q(iid=i[0])
        c = Cart.objects.filter(q1 & q2)
        context = {}
        context['data'] = i
        if len(c)==0:
            c=Cart.objects.create(uid=u[0],iid=i[0])  # as foreign key is used we have to pass the list's index position
            c.save()            
            context['success']="Icecream Added Successfully in the Cart"
            return render(request,'icecreamdetails2.html',context)
        else:
            context['errmsg']="Icecream already exists in the cart.."
            return render(request,'icecreamdetails2.html',context)
    else:
        return redirect('/login')

def cart(request):
    if request.user.is_authenticated:
        
        c=Cart.objects.filter(uid=request.user.id)
        print("cart:",c)
        context={}
        context['data']=c
        if len(c) ==0:
            context['errzero']="No Products in the Cart"
        s = 0
        for i in c:
            s = s+i.iid.price*i.qty
        context['total']=s
        context['n']=len(c)
        return render(request,'cart.html',context)   
    else:
         return redirect('/login')

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    print(c)
    q=c[0].qty
    print(q)
    if x=='1':
        q = q+1
    elif q > 1:
        q=q-1
    c.update(qty=q)
    return redirect('/cart')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    print(c)
    c.delete()
    return redirect('/cart')

def checkout(request):
    c=Cart.objects.filter(uid=request.user.id)

    for i in c:
        amt=i.qty*i.iid.price
        o=Order.objects.create(uid=i.uid, iid=i.iid, qty=i.qty, amt=amt)
        o.save()
        i.delete()          
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    context={}
    s=0
    for i in o:
        s=s+i.amt
    context['data']=o
    context['total']=s
    context['n']=len(o)
    ui = UserInfo.objects.filter(uid=request.user.id)
    context['data1'] = ui
    return render(request,'checkout.html',context)

def makepayments(request):
    # client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
    client = razorpay.Client(auth=("rzp_test_zHsTle7MWq2Hm8", "m5rOC7ES9NCZIWE1r4nVWHfq"))

    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt
    
    data = { "amount": s * 100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['payment']=payment
    return render(request, 'pay.html', context)

def payment_success(request):
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt
        
    for i in o:
        oh=OrderHistory.objects.create(uid=i.uid, iid=i.iid, qty=i.qty, amt=i.amt)
        i.delete()
        oh.save()
    sub='Order Status'
    msg='Order Placed Successfully...!!!'
    frm='rohitpalekar0027@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False

    )
    u=User.objects.filter(id=request.user.id)
    
    context={}
    
    context['total']=s
    ui = UserInfo.objects.filter(uid=request.user.id)
    context['data'] = u
    context['data1'] = ui
    return render(request,'payment_success.html',context)

def icecreamdetails(request,iid):
    print(iid)
    i = IcecreamInfo.objects.filter(id=iid)
    print('ice creme',i)
    context = {}
    context['data'] = i
    return render(request,'icecreamdetails.html',context)


def icecreamdetails2(request,iid):
    print(iid)
    i = IcecreamInfo.objects.filter(id=iid)
    print('ice creme',i)
    context = {}
    context['data'] = i
    return render(request,'icecreamdetails2html',context)
    

def fruitnnut(request):
    io = IcecreamInfo.objects.filter(category='Fruit-N-Nut')
    context = {}
    context['data'] = io
    return render(request,'fruitnnut.html',context)

def internationalpremium(request):
    io = IcecreamInfo.objects.filter(category='International-Premium')
    context = {}
    context['data'] = io
    return render(request,'internationalpremium.html',context)

def internationalclassic(request):
    io = IcecreamInfo.objects.filter(category='International-Classic')
    context = {}
    context['data'] = io
    return render(request,'internationalclassic.html',context)

def indianinspiration(request):
    io = IcecreamInfo.objects.filter(category='Indian-Inspiration')
    context = {}
    context['data'] = io
    return render(request,'indianinspiration.html',context)

def superpremium(request):
    io = IcecreamInfo.objects.filter(category='Super-Premium')
    context = {}
    context['data'] = io
    return render(request,'superpremium.html',context)

# user-profile function based view
def user_profile(request):
    if request.method == "GET":
        u = User.objects.filter(id=request.user.id)
        ui = UserInfo.objects.filter(uid=request.user.id)
        context = {}
        context['data'] = u
        if len(ui) ==0:
            context['size'] = "No data"
        else:
            context['data1'] = ui
        print('user',u)
        print('user info',ui)
        print('Length: ',len(ui))
        return render(request,'user_profile.html',context)

def edit_user_profile(request):
    if request.method == "GET":
        print('GET METHOD')
        u = User.objects.filter(id=request.user.id)
        ui = UserInfo.objects.filter(uid=request.user.id)
        context = {}
        context['data'] = u
        if len(ui) ==0:
            context['size'] = "No data"
        else:
            context['data1'] = ui
        return render(request,'edit_user_profile.html',context)
    else:
        print('POST METHOD')
        fn = request.POST['fname']
        ln = request.POST['lname']
        e = request.POST['email']
        m = request.POST['mob']
        addr = request.POST['address']
        print(fn,ln,e,m)
        u = User.objects.filter(id=request.user.id)        
        ui = UserInfo.objects.filter(uid=request.user.id)
        if len(ui)==0:
            uie = UserInfo.objects.create(uid=u[0], mobile=m, address=addr)
        else:
            ui.update(mobile = m,address=addr)
        u.update(first_name=fn,last_name=ln,email=e)
        return redirect('/user_profile')

def orderhistory(request):
    oh=OrderHistory.objects.filter(uid=request.user.id)
    print('order history',oh)
    context = {}
    context['data'] = oh
    return render(request,'order_history.html',context)

