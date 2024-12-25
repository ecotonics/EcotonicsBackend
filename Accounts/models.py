from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Technicians.models import Technician
from Works.models import Work

# Create your models here.

TRANSACTION = (
    ('INCOME','INCOME'),
    ('EXPENSE','EXPENSE'),
)

SOURCE = (
    ('PETTY','PETTY'),
    ('SELF','SELF'),
    ('CREDIT','CREDIT'),
)

class TransactionCategory(BaseModel):
    type = models.CharField(max_length=50,choices=TRANSACTION)
    name = models.CharField(max_length=100)
    info = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Transaction Category')
        verbose_name_plural = _('Transaction Categories')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(TransactionCategory, self).save(*args, **kwargs)

class BankAccount(BaseModel):
    name = models.CharField(max_length=100)
    account = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(BankAccount, self).save(*args, **kwargs)

class Transaction(BaseModel):
    date = models.DateField()
    type = models.CharField(max_length=25,choices=TRANSACTION)
    category = models.ForeignKey(TransactionCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    account = models.ForeignKey(BankAccount,on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)

        super(Transaction, self).save(*args, **kwargs)


class Expense(BaseModel):
    date = models.DateField(auto_now_add=True)
    work = models.ForeignKey(Work,on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician,on_delete=models.SET_NULL,null=True)

    category = models.ForeignKey(TransactionCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=250,null=True)
    source = models.CharField(max_length=50,choices=SOURCE)
    amount = models.FloatField(default=0.00)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)

        super(Expense, self).save(*args, **kwargs)