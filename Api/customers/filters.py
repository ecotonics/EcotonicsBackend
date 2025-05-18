import django_filters

from Customers.models import Customer


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['name','type','status']