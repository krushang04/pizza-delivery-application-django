from typing_extensions import ParamSpecKwargs
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pizzaapp import models
from django.contrib.auth.models import User
# Create your views here.
def adminloginview(request):
    return render(request,'adminlogin.html')

def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)

    if user is not None:
        login(request,user)
        return redirect('adminhomepage')


    if user is None:
        messages.add_message(request,messages.ERROR,"invalid credentials")
        return redirect('adminloginpage')

def adminhomepageview(request):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    context = {'pizza':models.PizzaModel.objects.all(),'users':User.objects.all(),'orders':models.OrderModel.objects.all()}
    return render(request,'adminhomepage.html',context)

def logoutadmin(request):
    logout(request)
    return redirect("adminloginpage")

def addpizza(request):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    name = request.POST['pizza']
    price = request.POST['price']
    if name!='' and price!='':
        models.PizzaModel(name=name,price=price).save()
    return redirect('adminhomepage')

def delpizza(request,id):
    if not request.user.is_authenticated:
        return redirect('adminloginpage')
    models.PizzaModel.objects.filter(id=id).delete()
    return redirect('adminhomepage')

def adminorders(request):
    context = {'orders':models.OrderModel.objects.all()}
    return render(request,'adminorders.html',context)
    
def acceptorder(request,orderid):
    obj = models.OrderModel.objects.filter(id = orderid)[0]
    obj.status = "Accepted"
    obj.save()
    return redirect(request.META['HTTP_REFERER'])

def declineorder(request,orderid):
    obj = models.OrderModel.objects.filter(id = orderid)[0]
    obj.status = "Declined"
    obj.save()
    return redirect(request.META['HTTP_REFERER'])

def homepage(request):
    return render(request,'homepage.html')

def signupuser(request):
    username =request.POST['username']
    password =request.POST['password']
    phoneno =request.POST['phoneno']

    if(User.objects.filter(username = username).exists()):
        messages.add_message(request,messages.ERROR,"User Already Exists!")
        return redirect('homepage')
    User.objects.create_user(username = username,password=password).save()
    lastobj = len(User.objects.all())-1
    models.CustomerModel(userid = User.objects.all()[lastobj].id,phoneno = phoneno).save()
    messages.add_message(request,messages.ERROR,"User SuccessFully Created!")
    return redirect('homepage')

def userloginview(request):
    return render(request,'userloginpage.html')

def authenticateuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)

    if user is not None:
        login(request,user)
        return redirect('customerpage')


    if user is None:
        messages.add_message(request,messages.ERROR,"invalid credentials")
        return redirect('userloginpage')

def customerwelcome(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username = request.user.username
    context = {'username':username,'pizza':models.PizzaModel.objects.all()}
    return render(request,'customerwel.html',context)

def userlogout(request):
    logout(request)
    return redirect('userloginpage')

def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username = request.user.username 
    phoneno = models.CustomerModel.objects.filter(userid=request.user.id)[0].phoneno
    address = request.POST['address']
    
    tp = 0
    tq = 0
    for p in models.PizzaModel.objects.all():
        pid = p.id
        name = p.name
        price = int(p.price)
        qnt = str(request.POST.get(str(pid),""))
        if qnt!="0" and qnt!="":
            tq = tq + int(qnt) 
            tp = tp + price*int(qnt) 
    
    ordereditems = str(tq)+' '+str(tp)
    models.OrderModel(username = username,phoneno = phoneno, address = address,
    ordereditems = ordereditems).save()
    messages.add_message(request,messages.ERROR,"Order Placed Successfully")
    # context = {'orders':models.OrderModel.objects.filter(username = request.user.username)}
    # return render(request,'userorders.html',context)
    return redirect('customerpage')

def userorders(request):
    context = {'orders':models.OrderModel.objects.filter(username = request.user.username)}
    return render(request,'userorders.html',context)