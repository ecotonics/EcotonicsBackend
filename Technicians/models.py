from django.db import models
from Users.models import User
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware

# Create your models here.

class Department(BaseModel):
    name = models.CharField(max_length=50)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Department, self).save(*args, **kwargs)

class Designation(BaseModel):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(Designation, self).save(*args, **kwargs)

class Technician(BaseModel):
    status = models.IntegerField(default=1)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    aadhar = models.CharField(max_length=12)
    blood = models.CharField(max_length=3)
    department = models.OneToOneField(Department,on_delete=models.SET_NULL,null=True)
    designation = models.OneToOneField(Designation,on_delete=models.SET_NULL,null=True)
    contact_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    relation = models.CharField(max_length=50)
    address = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = _('Technician')
        verbose_name_plural = _('Technicians')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.user.username)

        super(Technician, self).save(*args, **kwargs)