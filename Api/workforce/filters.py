import django_filters

from Workforce.models import Department, Designation, Staff

class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Department
        fields = ['name',]


class DesignationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Designation
        fields = ['name', 'department']


class StaffFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Staff
        fields = ['name','designation','department','status']