from Workforce.models import Department, Designation, Staff
from Users.models import User
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
    department_id = serializers.SerializerMethodField()
    staffs = serializers.SerializerMethodField()

    class Meta:
        model = Designation
        fields = ['id','slug','name','info','department','department_name','department_id','staffs']
    
    def get_department_name(self, designation):
        return designation.department.name
    
    def get_department_id(self, designation):
        return designation.department.id
    
    def get_staffs(self, designation):
        return Staff.objects.filter(designation=designation).count()
    

class UserSerializer(RepMixin, serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'photo', 'mobile']
        extra_kwargs = {
            'first_name': {'required': True},
            'mobile': {'required': True},
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class StaffSerializer(RepMixin, serializers.ModelSerializer):
    department_data = DepartmentSerializer(source='department', read_only=True)
    designation_data = DesignationSerializer(source='designation', read_only=True)
    user_data = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id','slug','user','designation','department','status','department_data','designation_data','user_data',
            'location','aadhar','blood','contact_name','contact_number','relation','address','staff_wage'
        ]