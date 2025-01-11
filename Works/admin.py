from django.contrib import admin
from Works.models import Requisition, RequisitionItem, Work, Attendance

# Register your models here.

class WorkAdmin(admin.ModelAdmin):
    list_display = ['lead','status','is_deleted']

admin.site.register(Work, WorkAdmin)

class RequisitionAdmin(admin.ModelAdmin):
    list_display = ['work','date','prepared','status','is_deleted']

admin.site.register(Requisition, RequisitionAdmin)

class RequisitionItemAdmin(admin.ModelAdmin):
    list_display = ['requisition', 'name', 'unit', 'quantity']

admin.site.register(RequisitionItem, RequisitionItemAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date','status','staff','work','start_time','end_time','is_deleted']

admin.site.register(Attendance, AttendanceAdmin)