from django.contrib import admin
from Users.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','is_superuser','is_technician']

admin.site.register(User, UserAdmin)