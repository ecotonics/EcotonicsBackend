from django.contrib import admin
from Customers.models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','type','location','mobile','email','status']

admin.site.register(Customer, CustomerAdmin)