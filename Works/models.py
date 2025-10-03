from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Customers.models import Customer
from Workforce.models import Staff
from Users.models import User
from Services.models import Category, Service
from Core.choices import OnCallStatusChoices, CustomerTypeChoices
# from Accounts.models import Wage

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

TASK_STATUS = (
    ('PENDING', 'PENDING'),
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

class OnCall(BaseModel):
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=OnCallStatusChoices.choices, default=OnCallStatusChoices.PENDING)
    type = models.CharField(max_length=50, choices=CustomerTypeChoices.choices)

    customer = models.ForeignKey(Customer,on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    service = models.ForeignKey(Service,on_delete=models.PROTECT)

    site_name = models.CharField(max_length=100)
    info = models.TextField(null=True,blank=True)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=25, null=True, blank=True)
    site_location = models.TextField(null=True, blank=True)

    staffs = models.ManyToManyField(Staff, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = _('On Call')
        verbose_name_plural = _('On Calls')
        ordering = ("-date",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.site_name)

        super(OnCall, self).save(*args, **kwargs)


class Attendance(BaseModel):
    date = models.DateField()
    status = models.CharField(default='PENDING', max_length=20)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    wage = models.FloatField(default=0.00)
    on_call = models.ForeignKey(OnCall, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.staff.user.first_name}'

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
        ordering = ("-date",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.staff.user.username)

        super(Attendance, self).save(*args, **kwargs)


class Task (BaseModel):
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ("-date",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)

        super(Task, self).save(*args, **kwargs)