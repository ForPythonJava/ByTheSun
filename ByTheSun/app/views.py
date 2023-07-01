from django.shortcuts import (
    render,
    HttpResponseRedirect,
    redirect,
    HttpResponsePermanentRedirect,
)
from .models import *
from django.db.models import Q, Sum
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
            elif user.userType == "Service Centre":
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
    categories = Category.objects.all()
    if request.POST:
        name = request.POST["name"]
        image = request.FILES["imgfile"]
        category = request.POST["category"]
        qty = request.POST["qty"]
        price = request.POST["price"]
        desc = request.POST["desc"]
        addPdt = Product.objects.create(
            name=name,
            category=category,
            quantity=qty,
            price=price,
            image=image,
            description=desc,
        )
        addPdt.save()
        messages.success(request, "Product Added")
    return render(request, "ADMIN/addProduct.html", {"categories": categories})


def viewProductsAdmin(request):
    products = Product.objects.all()
    return render(request, "ADMIN/viewProductsAdmin.html", {"products": products})


def updateProduct(request):
    id = request.GET["id"]
    pdtData = Product.objects.get(id=id)
    categories = Category.objects.all()
    if request.POST:
        name = request.POST["name"]
        image = request.FILES.get("imgfile")
        category = request.POST["category"]
        qty = request.POST["qty"]
        price = request.POST["price"]
        desc = request.POST["desc"]
        pdtData.name = name
        pdtData.category = category
        pdtData.quantity = qty
        pdtData.price = price
        pdtData.description = desc
        if image:
            pdtData.image = image
        else:
            pdtData.image = pdtData.image
        pdtData.save()
        return redirect("/viewProductsAdmin")
    return render(
        request,
        "ADMIN/updateProduct.html",
        {"pdtData": pdtData, "categories": categories},
    )


def adminViewOrders(request):
    myOrders = Cart.objects.filter(Q(status="Paid"))
    return render(request, "ADMIN/adminViewOrders.html", {"myOrders": myOrders})


def viewFeedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, "ADMIN/viewFeedback.html", {"feedbacks": feedbacks})


def sellingRequests(request):
    viewData = SellingRequest.objects.all()
    return render(request, "ADMIN/sellingRequests.html", {"viewData": viewData})


def manageRequest(request):
    id = request.GET["id"]
    status = request.GET["status"]
    updateData = SellingRequest.objects.filter(id=id).update(status=status)
    messages.success(request, f"Request {status}")
    return redirect("/sellingRequests")


####################################################--CUSTOMER--#########################################################


def viewProducts(request):
    pdtData = Product.objects.all()
    return render(request, "CUSTOMER/viewProducts.html", {"pdtData": pdtData})


def addToCart(request):
    uid = request.session["uid"]
    userid = Customer.objects.get(loginid__id=uid)
    if request.POST:
        id = request.POST["id"]
        stock = request.POST["stock"]
        quantity = request.POST["qty"]
        rate = request.POST["rate"]

        pid = Product.objects.get(id=id)
        total = int(quantity) * int(rate)
        uStock = int(stock) - int(quantity)

        print("Total", total)
        print("Stock", uStock)
        if Cart.objects.filter(
            Q(uid=userid) & Q(pid=pid) & Q(status="InCart")
        ).exists():
            messages.error(request, "Already Added")
            return redirect("/viewCart")
        else:
            addCart = Cart.objects.create(
                uid=userid, pid=pid, quantity=quantity, price=total
            )
            addCart.save()
            updateStock = Product.objects.filter(id=id).update(quantity=uStock)
            messages.success(request, "Added To Cart Successfully")
    return redirect("/viewProducts")


def viewCart(request):
    uid = request.session["uid"]
    myCart = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="InCart"))
    if not myCart.exists():
        messages.error(request, "Cart Is Empty")
        return redirect("/viewProducts")
    print(myCart)
    cartTotal = Cart.objects.filter(
        Q(uid_id__loginid__id=uid) & Q(status="InCart")
    ).aggregate(total=Sum("price"))["total"]
    print(cartTotal)
    # if cartTotal is None:
    #     return redirect("/customerHome")
    count = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="InCart")).count()
    return render(
        request,
        "CUSTOMER/myCart.html",
        {"myCart": myCart, "cartTotal": cartTotal, "count": count},
    )


def removeFromCart(request):
    id = request.GET["id"]
    pid = request.GET["pid"]
    qty = request.GET["qty"]

    updatePdt = Product.objects.get(id=pid)
    stock = updatePdt.quantity
    uStock = int(stock) + int(qty)
    updatePdt.quantity = uStock
    updatePdt.save()
    updateCart = Cart.objects.get(id=id).delete()
    return redirect("/viewCart")


def paymentForm(request):
    id = request.GET["id"]
    cartData = Cart.objects.get(id=id)
    cartTotal = cartData.price
    if request.POST:
        updateStatus = Cart.objects.filter(id=id).update(status="Paid")
        messages.success(request, "Payment Success")
        return redirect("/viewOrders")
    return render(request, "CUSTOMER/paymentForm.html", {"cartTotal": cartTotal})


def checkOut(request):
    uid = request.session["uid"]
    myCart = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="InCart"))
    id_list = myCart.values_list("id", flat=True)
    cartTotal = Cart.objects.filter(
        Q(uid_id__loginid__id=uid) & Q(status="InCart")
    ).aggregate(total=Sum("price"))["total"]
    print(id_list)
    for i in id_list:
        print(i)

    if request.POST:
        for i in id_list:
            updateStatus = Cart.objects.filter(id=i).update(status="Paid")
        return redirect("/viewOrders")
    return render(request, "CUSTOMER/paymentForm.html", {"cartTotal": cartTotal})


def viewOrders(request):
    uid = request.session["uid"]
    myOrders = Cart.objects.filter(Q(uid_id__loginid__id=uid) & Q(status="Paid"))
    return render(request, "CUSTOMER/viewOrders.html", {"myOrders": myOrders})


def addFeedback(request):
    uid = request.session["uid"]
    if request.POST:
        title = request.POST["title"]
        feedback = request.POST["feedback"]
        userid = Customer.objects.get(loginid__id=uid)
        addFdbk = Feedback.objects.create(title=title, feedback=feedback, uid=userid)
        addFdbk.save()
        messages.success(request, "Feedback Added")
    return render(request, "CUSTOMER/addFeedback.html")


def customerViewService(request):
    centreData = Shop.objects.filter(loginid_id__is_active=1)
    print(centreData)
    return render(
        request, "CUSTOMER/viewServiceCentre.html", {"centreData": centreData}
    )


def addProblem(request):
    curr_date = datetime.today().strftime("%Y-%m-%d")
    print(curr_date)
    uid = request.session["uid"]
    userid = Customer.objects.get(loginid__id=uid)
    id = request.GET["id"]
    shopid = Shop.objects.get(id=id)
    if request.POST:
        problem = request.POST["problem"]
        date = request.POST["date"]
        bookDate = Booking.objects.create(
            uid=userid, shopid=shopid, problem=problem, date=date
        )
        bookDate.save()
        messages.success(request, "Booking Successfull")
        return redirect("/viewBookings")
    return render(request, "CUSTOMER/addProblem.html", {"curr_date": curr_date})


def viewBookings(request):
    uid = request.session["uid"]
    bookData = Booking.objects.filter(uid__loginid__id=uid)
    return render(request, "CUSTOMER/viewBookings.html", {"bookData": bookData})


def addSellingRequest(request):
    uid = request.session["uid"]
    userid = Customer.objects.get(loginid__id=uid)
    if request.POST:
        unit = request.POST["unit"]
        addRequest = SellingRequest.objects.create(unit=unit, uid=userid)
        addRequest.save()
        messages.success(request, "Request Sent")
        return redirect("/viewStatus")
    return render(request, "CUSTOMER/addSellingRequest.html")


def viewStatus(request):
    viewData = SellingRequest.objects.all()
    return render(request, "CUSTOMER/viewStatus.html", {"viewData": viewData})


####################################################--SERVICE CENTRE--###################################################


def serviceBookings(request):
    uid = request.session["uid"]
    bookData = Booking.objects.filter(shopid__loginid__id=uid)
    return render(request, "SERVICE/viewBookings.html", {"bookData": bookData})


def serviceHome(request):
    return render(request, "SERVICE/serviceHome.html")


def manageBooking(request):
    id = request.GET["id"]
    status = request.GET["status"]

    updateData = Booking.objects.filter(id=id).update(status=status)
    messages.success(request, f"Successfully {status}")
    return redirect("/serviceBookings")
