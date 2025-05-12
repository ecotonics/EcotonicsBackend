from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from Core.choices import CategoryStatusChoices, ServiceStatusChoices
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=25, choices=CategoryStatusChoices.choices, default=CategoryStatusChoices.ACTIVE)

    info = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ("name",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Category, self).save(*args, **kwargs)

class Service(BaseModel):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=25, choices=ServiceStatusChoices.choices, default=ServiceStatusChoices.ACTIVE)

    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    info = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ("name",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Service, self).save(*args, **kwargs)