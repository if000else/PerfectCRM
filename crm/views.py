from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# from django import conf
# from kingadmin import app_config
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')
@login_required
def customer_list(request):

    return render(request,'sales/customers.html',)

def acc_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)
        if user:
            #auth pass
            login(request,user)

            return redirect("/crm")

    return render(request,"login.html")


def acc_logout(request):

    logout(request)

    return redirect("/login")