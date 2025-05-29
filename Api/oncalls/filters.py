import django_filters

from Works.models import OnCall

class OnCallFilter(django_filters.FilterSet):
    site_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OnCall
        fields = [
            'site_name', 'status', 'type', 'customer', 'category', 'service', 'staffs'
        ]