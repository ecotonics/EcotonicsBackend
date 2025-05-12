import django_filters

from Workforce.models import Department, Designation

class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Department
        fields = ['name',]


class DesignationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Designation
        fields = ['name',]