from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Services.models import Category, Service
from Workforce.models import Staff

# Create your models here.

TYPE = (
    ('individual', 'individual'),
    ('enterprise', 'enterprise')
)

LEAD_STATUS = (
    ('PENDING', 'PENDING'),
    ('CONVERTED', 'CONVERTED'),
    ('FAILED', 'FAILED')
)

CUSTOMER_STATUS = (
    ('active','Active'),
    ('inactive','Inactive'),
)

class Customer(BaseModel):
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=TYPE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ("name",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Customer, self).save(*args, **kwargs)


class Lead(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=LEAD_STATUS, default='PENDING')
    is_update_allowed = models.BooleanField(default=True)

    type = models.CharField(max_length=50, choices=TYPE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    service = models.ForeignKey(Service,on_delete=models.PROTECT)
    info = models.TextField(null=True,blank=True)

    primary_requirements = models.TextField(null=True, blank=True)
    scope_of_work = models.TextField(null=True, blank=True)
    site_condetion = models.TextField(null=True, blank=True)
    additional_requirements = models.TextField(null=True, blank=True)
    customer_preferences = models.TextField(null=True, blank=True)

    staffs = models.ManyToManyField(Staff)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Lead')
        verbose_name_plural = _('Leads')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Lead, self).save(*args, **kwargs)

class Followup(BaseModel):
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    details = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = _('Followup')
        verbose_name_plural = _('Followups')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)

        super(Followup, self).save(*args, **kwargs)