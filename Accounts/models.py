from django.db import models
from Core.models import BaseModel
from Core.models import save_data
from django.utils.translation import gettext_lazy as _
from Core.middlewares import RequestMiddleware

# Create your models here.

class TransactionCategory(BaseModel):
    name = models.CharField(max_length=100)
    info = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Transaction Category')
        verbose_name_plural = _('Transaction Categories')
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)

        super(TransactionCategory, self).save(*args, **kwargs)