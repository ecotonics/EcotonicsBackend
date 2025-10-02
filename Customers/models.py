from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Services.models import Category, Service
from Workforce.models import Staff
from Core.choices import CustomerTypeChoices, CustomerStatusChoices

# Create your models here.

class Customer(BaseModel):
    status = models.CharField(max_length=50, choices=CustomerStatusChoices.choices, default=CustomerStatusChoices.ACTIVE)
    type = models.CharField(max_length=50, choices=CustomerTypeChoices.choices)
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