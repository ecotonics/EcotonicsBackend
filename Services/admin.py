from django.contrib import admin
from Services.models import Category, Service

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','info','is_deleted']

admin.site.register(Category, CategoryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name','slug','category','is_deleted']

admin.site.register(Service, ServiceAdmin)