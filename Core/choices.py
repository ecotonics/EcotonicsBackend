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

class CustomerStatusChoices(models.TextChoices):
    ACTIVE = 'active',_('Active')
    INACTIVE = 'inactive',_('Inactive')

class CustomerTypeChoices(models.TextChoices):
    INDIVIDUAL = 'individual',_('Individual')
    ENTERPRISE = 'enterprise',_('Enterprise')
    
class OnCallStatusChoices(models.TextChoices):
    PENDING = 'pending',_('Pending')
    ONGOING = 'ongoing',_('Ongoing')
    COMPLETED = 'completed',_('Completed')
    CANCELLED = 'cancelled',_('Cancelled')