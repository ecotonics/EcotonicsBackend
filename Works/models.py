from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware
from Customers.models import Lead
from Technicians.models import Technician

# Create your models here.

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