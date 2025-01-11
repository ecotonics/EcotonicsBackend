from django.contrib import admin
from Accounts.models import TransactionCategory,BankAccount,Transaction

# Register your models here.

class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['type','name','is_deleted']

admin.site.register(TransactionCategory, TransactionCategoryAdmin)


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name','account','number','branch','is_deleted']

admin.site.register(BankAccount, BankAccountAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date','type','category','title','account','amount','is_deleted']

admin.site.register(Transaction, TransactionAdmin)