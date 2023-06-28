from django.shortcuts import (
    render,
    HttpResponseRedirect,
    redirect,
    HttpResponsePermanentRedirect,
)
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, "index.html")


def logout(request):
    request.session.clear()
    messages.success(request, "Logged Out")
    return HttpResponseRedirect("/login")


def customerHome(request):
    return render(request, "CUSTOMER/customerHome.html")


def adminHome(request):
    return render(request, "ADMIN/adminHome.html")


def contact(request):
    return render(request, "contact.html")


def signin(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        print(email)
        print(passw)
        user = authenticate(username=email, password=passw)
        print(user)
        if user is not None:
            login(request, user)
            if user.userType == "Admin":
                id = user.id
                request.session["uid"] = id
                request.session["type"] = "Admin"
                messages.info(request, "Login Success")
                return redirect("/adminHome")
            elif user.userType == "Customer":
                id = user.id
                request.session["uid"] = id
                request.session["type"] = "Child"
                messages.info(request, "Login Success")
                return redirect("/customerHome")
            elif user.userType == "Service":
                id = user.id
                request.session["uid"] = id
                messages.info(request, "Login Success")
                return redirect("/serviceHome")
        else:
            print("Hiii")
            messages.error(request, "Invalid Username/Password")
    return render(request, "COMMON/login.html")


def customerReg(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        district = request.POST["district"]
        password = request.POST["password"]
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Customer",
                viewPass=password,
                is_active=1,
            )
            logQry.save()
            regQry = Customer.objects.create(
                name=name,
                email=email,
                phone=phone,
                district=district,
                address=address,
                loginid=logQry,
            )
            regQry.save()
            messages.success(request, "Registered Successfully")
            return redirect("/login")
    return render(request, "COMMON/customer.html")


def serviceReg(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        district = request.POST["district"]
        password = request.POST["password"]
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Service Centre",
                viewPass=password,
                is_active=0,
            )
            logQry.save()
            regQry = Shop.objects.create(
                name=name,
                email=email,
                phone=phone,
                district=district,
                address=address,
                loginid=logQry,
            )
            regQry.save()
            messages.success(request, "Registered Successfully")
            return redirect("/login")
    return render(request, "COMMON/servicereg.html")


#####################################################--ADMIN--###########################################################


def viewUsers(request):
    userData = Customer.objects.all()
    return render(request, "ADMIN/viewUsers.html", {"userData": userData})


def deleteUser(request):
    id = request.GET["id"]
    deleteUser = Login.objects.filter(id=id).delete()
    return redirect("/viewUsers")


def viewServiceCenter(request):
    serviceData = Shop.objects.all()
    return render(request, "ADMIN/viewServiceCenter.html", {"serviceData": serviceData})


def manageService(request):
    id = request.GET["id"]
    data = Login.objects.get(id=id)
    data.is_active = 1
    data.save()
    return redirect("/viewServiceCenter")


def addCategory(request):
    if request.POST:
        category = request.POST["category"]
        addCat = Category.objects.create(category=category)
        addCat.save()
        return redirect("/addCategory")
    return render(request, "ADMIN/addCategory.html")


def viewCategory(request):
    categories = Category.objects.all()
    return render(request, "ADMIN/viewCategory.html", {"categories": categories})


def deleteService(request):
    id = request.GET["id"]
    deleteCat = Category.objects.get(id=id).delete()
    return redirect("/viewCategory")


def addProduct(request):
    # if request.POST:

    return render(request, "ADMIN/addProduct.html")
