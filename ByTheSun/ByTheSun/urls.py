"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('contact/', views.contact),
    path('', views.index),
    path('login/', views.signin),
    path('customer/', views.customerReg),
    path('customerHome/', views.customerHome),
    path('logout/', views.logout),
    path('adminHome/', views.adminHome),
    path('viewUsers/', views.viewUsers),
    path('deleteUser/', views.deleteUser),
    path('viewServiceCenter/', views.viewServiceCenter),
    path('serviceReg/', views.serviceReg),
    path('manageService/', views.manageService),
    path('addCategory/', views.addCategory),
    path('viewCategory/', views.viewCategory),
    path('deleteService/', views.deleteService),
    path('addProduct/', views.addProduct),

]
