from django.contrib import admin
from Works.models import Requisition, RequisitionItem, Work, Attendance

# Register your models here.

class RequisitionAdmin(admin.ModelAdmin):
    list_display = ['lead','date','prepared','status','is_deleted']

admin.site.register(Requisition, RequisitionAdmin)

class RequisitionItemAdmin(admin.ModelAdmin):
    list_display = ['requisition', 'name', 'unit', 'quantity']

admin.site.register(RequisitionItem, RequisitionItemAdmin)

class WorkAdmin(admin.ModelAdmin):
    list_display = ['lead','status','is_deleted']

admin.site.register(Work, WorkAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date','status','technician','work','start_time','end_time','is_deleted']

admin.site.register(Attendance, AttendanceAdmin)