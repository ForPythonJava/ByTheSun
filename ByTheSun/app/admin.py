from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(Login)
admin.site.register(Product)
admin.site.register(Cart)
