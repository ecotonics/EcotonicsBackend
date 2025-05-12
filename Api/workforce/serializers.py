from Workforce.models import Department, Designation, Staff
from rest_framework import serializers
from Core.mixins import RepMixin

class DepartmentSerializer(RepMixin, serializers.ModelSerializer):
    designations = serializers.SerializerMethodField()
    staffs = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id','slug','name','info','designations','staffs']

    def get_designations(self, department):
        return Designation.objects.filter(department=department).count()

    def get_staffs(self, department):
        return Staff.objects.filter(department=department).count()


class DesignationSerializer(RepMixin, serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    department_slug = serializers.SerializerMethodField()
    staffs = serializers.SerializerMethodField()

    class Meta:
        model = Designation
        fields = ['id','slug','name','info','department','department_name','department_slug','staffs']
    
    def get_department_name(self, designation):
        return designation.department.name
    
    def get_department_slug(self, designation):
        return designation.department.slug
    
    def get_staffs(self, designation):
        return Staff.objects.filter(designation=designation).count()
