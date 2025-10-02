from django.contrib import admin
from Accounts.models import TransactionCategory,BankAccount,Transaction, Wage
from import_export.admin import ExportMixin

# Register your models here.

class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['type','name','is_deleted']

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name','account','number','branch','is_deleted']

class TransactionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['date','type','category','title','account','amount','is_deleted']

class WageAdmin(admin.ModelAdmin):
    list_display = ['staff','updated','amount','is_deleted']


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(TransactionCategory, TransactionCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wage, WageAdmin)