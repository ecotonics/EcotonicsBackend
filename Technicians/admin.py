from django.contrib import admin
from Technicians.models import Department, Designation, Technician

# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','slug','is_deleted']

admin.site.register(Department, DepartmentAdmin)

class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name','slug','department','is_deleted']

admin.site.register(Designation, DesignationAdmin)

class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['user','department','designation','is_deleted']

admin.site.register(Technician, TechnicianAdmin)