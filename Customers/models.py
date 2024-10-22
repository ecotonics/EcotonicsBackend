from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Services.models import Category, Service

# Create your models here.

class Customer(BaseModel):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Customer, self).save(*args, **kwargs)


class Lead(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,default='PENDING')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    service = models.ForeignKey(Service,on_delete=models.PROTECT)
    info = models.TextField(null=True,blank=True)

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