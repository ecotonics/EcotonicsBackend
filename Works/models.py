from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Customers.models import Lead, Customer
from Workforce.models import Staff
from Users.models import User
from Services.models import Category, Service

UNITS = (
    ('NOS','NOS'),
    ('METERS','METERS'),
    ('KILOGRAMS','KILOGRAMS'),
)

WORK_STATUS = (
    ('PENDING', 'PENDING'),
    ('ONGOING', 'ONGOING'),
    ('COMPLETED', 'COMPLETED')
)

TYPE = (
    ('individual', 'individual'),
    ('enterprise', 'enterprise')
)

LEAD_STATUS = (
    ('PENDING', 'PENDING'),
    ('CONVERTED', 'CONVERTED'),
    ('FAILED', 'FAILED')
)

class Work(BaseModel):
    status = models.CharField(max_length=20, choices=WORK_STATUS, default='PENDING')
    date = models.DateField(auto_now_add=True)
    lead = models.OneToOneField(Lead,on_delete=models.CASCADE)
    staffs = models.ManyToManyField(Staff)

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

class Requisition(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='PENDING')
    prepared = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    def __str__(self):
        return self.work.lead.name
    
    class Meta:
        verbose_name = _('Requisition')
        verbose_name_plural = _('Requisitions')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.work.lead.name)

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

class OnCall(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=LEAD_STATUS, default='PENDING')
    type = models.CharField(max_length=50, choices=TYPE)

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    service = models.ForeignKey(Service,on_delete=models.PROTECT)

    site_name = models.CharField(max_length=100)
    info = models.TextField(null=True,blank=True)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=25, null=True, blank=True)
    site_location = models.TextField(null=True, blank=True)

    staffs = models.ManyToManyField(Staff)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = _('On Call')
        verbose_name_plural = _('On Calls')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.site_name)

        super(OnCall, self).save(*args, **kwargs)


class Attendance(BaseModel):
    date = models.DateField()
    status = models.CharField(default='PENDING', max_length=20)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    work = models.ForeignKey(Work,on_delete=models.CASCADE,null=True, blank=True)
    on_call = models.ForeignKey(OnCall, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.staff.user.first_name}'

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.staff.user.username)

        super(Attendance, self).save(*args, **kwargs)