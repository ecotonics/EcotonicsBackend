from django.contrib import admin
from Customers.models import Customer, Lead

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','type','location','mobile','email','is_deleted']

admin.site.register(Customer, CustomerAdmin)

class LeadAdmin(admin.ModelAdmin):
    list_display = ['name','type','status','location','mobile','email','category','service','is_deleted']

admin.site.register(Lead, LeadAdmin)