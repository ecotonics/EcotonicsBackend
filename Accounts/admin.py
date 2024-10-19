from django.contrib import admin
from Accounts.models import TransactionCategory,BankAccount

# Register your models here.

class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','is_deleted']

admin.site.register(TransactionCategory, TransactionCategoryAdmin)


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name','account','number','branch','is_deleted']

admin.site.register(BankAccount, BankAccountAdmin)