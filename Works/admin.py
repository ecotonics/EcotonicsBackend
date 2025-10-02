from django.contrib import admin
from Works.models import Attendance, OnCall

# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date','status','staff','start_time','end_time','is_deleted']

admin.site.register(Attendance, AttendanceAdmin)

class OnCallAdmin(admin.ModelAdmin):
    list_display = ['date','status','category','service','is_deleted']

admin.site.register(OnCall, OnCallAdmin)