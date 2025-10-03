from django.contrib import admin
from Works.models import Attendance, OnCall, Task

# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date','status','staff','start_time','end_time','is_deleted']

class OnCallAdmin(admin.ModelAdmin):
    list_display = ['date','status','category','service','is_deleted']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['date','title','is_completed','is_deleted']


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(OnCall, OnCallAdmin)
admin.site.register(Task, TaskAdmin)