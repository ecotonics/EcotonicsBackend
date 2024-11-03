from django.contrib import admin
from Works.models import Work

# Register your models here.

class WorkAdmin(admin.ModelAdmin):
    list_display = ['lead','status','is_deleted']

admin.site.register(Work, WorkAdmin)