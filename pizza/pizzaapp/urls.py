
from django.contrib import admin
from django.urls import path
from pizzaapp import views

urlpatterns = [
    path('admin/',views.adminloginview,name="adminloginpage"),
    path('admin/authenticateadmin',views.authenticateadmin),
    path('admin/homepage',views.adminhomepageview,name="adminhomepage"),
    path('admin/logoutadmin/',views.logoutadmin),
    path('admin/addpizza',views.addpizza),
    path('admin/delpizza/<int:id>',views.delpizza),
    path('admin/adminorders',views.adminorders),
    path('admin/acceptorder/<int:orderid>',views.acceptorder),
    path('admin/declineorder/<int:orderid>',views.declineorder),
    path('',views.homepage,name="homepage"),
    path('su',views.signupuser),
    path('login',views.userloginview,name='userloginpage'),
    path('me',views.customerwelcome,name="customerpage"),
    path('authenticateuser',views.authenticateuser),
    path('userlogout',views.userlogout),
    path('placeorder',views.placeorder),
    path('userorders',views.userorders),
    
]
