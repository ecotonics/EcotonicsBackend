from django.contrib import admin
from Services.models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','info']

admin.site.register(Category, CategoryAdmin)