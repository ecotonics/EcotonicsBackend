from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Workforce.models import Staff
from Works.models import Work, OnCall
from Customers.models import Customer, Lead

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

TRANSACTION_STATUS = (
    ('pending','PENDING'),
    ('approved','APPROVED'),
    ('rejected','REJECTED'),
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
        ordering = ("name",)

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
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS, default='pending')

    type = models.CharField(max_length=25, choices=TRANSACTION)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True, blank=True)
    on_call = models.ForeignKey(OnCall, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200)
    account = models.ForeignKey(BankAccount,on_delete=models.CASCADE, null=True, blank=True)
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
        save_data(self, request, self.category)

        super(Transaction, self).save(*args, **kwargs)