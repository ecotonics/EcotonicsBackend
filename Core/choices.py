from django.db import models
from django.utils.translation import gettext_lazy as _

class CategoryStatusChoices(models.TextChoices):
    ACTIVE = 'active',_('Active')
    INACTIVE = 'inactive',_('Inactive')

class ServiceStatusChoices(models.TextChoices):
    ACTIVE = 'active',_('Active')
    INACTIVE = 'inactive',_('Inactive')

class StaffStatusChoices(models.TextChoices):
    ACTIVE = 'active',_('Active')
    INACTIVE = 'inactive',_('Inactive')