from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    district = models.CharField(max_length=100)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    district = models.CharField(max_length=100)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="image")
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    uid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price=models.IntegerField()
    status = models.CharField(max_length=100, default="InCart")


class Feedback(models.Model):
    uid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    feedback=models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    status=models.CharField(max_length=100,default="Sent")


class Booking(models.Model):
    uid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    shopid=models.ForeignKey(Shop,on_delete=models.CASCADE)
    problem=models.CharField(max_length=300)
    date=models.DateField()
    status=models.CharField(max_length=100,default="Pending")
    
    
class SellingRequest(models.Model):
    uid=models.ForeignKey(Customer,on_delete=models.CASCADE)
    unit=models.IntegerField()
    status=models.CharField(max_length=100,default="Pending")
    date=models.DateField(auto_now=True)
