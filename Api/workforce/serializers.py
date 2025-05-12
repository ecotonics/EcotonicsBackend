from Workforce.models import Department, Designation, Staff
from rest_framework import serializers
from Core.mixins import RepMixin

class DepartmentSerializer(RepMixin, serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id','slug','name','info','employees']

    def get_employees(self, department):
        return Staff.objects.filter(department=department).count()


class DesignationSerializer(RepMixin, serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Designation
        fields = ['id','slug','name','info','employees']

    def get_employees(self, designation):
        return Staff.objects.filter(designation=designation).count()
