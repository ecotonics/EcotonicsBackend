from django.contrib import admin
from Works.models import Work, Attendance

# Register your models here.

class WorkAdmin(admin.ModelAdmin):
    list_display = ['lead','status','is_deleted']

admin.site.register(Work, WorkAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['date','status','technician','work','start_time','end_time','is_deleted']

admin.site.register(Attendance, AttendanceAdmin)