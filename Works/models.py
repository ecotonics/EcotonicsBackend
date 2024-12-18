from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Customers.models import Lead
from Technicians.models import Technician

UNITS = (
    ('NOS','NOS'),
    ('METERS','METERS'),
    ('KILOGRAMS','KILOGRAMS'),
)

# Create your models here.

class Requisition(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='PENDING')
    prepared = models.ForeignKey(Technician, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)

    def __str__(self):
        return self.lead.name
    
    class Meta:
        verbose_name = _('Requisition')
        verbose_name_plural = _('Requisitions')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.lead.name)

        super(Requisition, self).save(*args, **kwargs)

class RequisitionItem(BaseModel):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, choices=UNITS)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('RequisitionItem')
        verbose_name_plural = _('RequisitionItems')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(RequisitionItem, self).save(*args, **kwargs)

class Work(BaseModel):
    status = models.CharField(max_length=20,default='PENDING')
    date = models.DateField(auto_now_add=True)
    lead = models.ForeignKey(Lead,on_delete=models.CASCADE)
    technicians = models.ManyToManyField(Technician)

    def __str__(self):
        return self.lead.name

    class Meta:
        verbose_name = _('Work')
        verbose_name_plural = _('Works')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.lead.name)

        super(Work, self).save(*args, **kwargs)


class Attendance(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1)
    technician = models.ForeignKey(Technician,on_delete=models.CASCADE)
    work = models.ForeignKey(Work,on_delete=models.CASCADE)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.technician.user.first_name}'

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.technician.user.username)

        super(Attendance, self).save(*args, **kwargs)