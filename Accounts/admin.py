from django.contrib import admin
from Accounts.models import TransactionCategory

# Register your models here.

class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','is_deleted']

admin.site.register(TransactionCategory, TransactionCategoryAdmin)