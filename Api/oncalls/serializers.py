from Works.models import OnCall
from rest_framework import serializers
from Core.mixins import RepMixin
from Api.customers.serializers import CustomerSerializer
from Api.services.serializers import CategorySerializer, ServiceSerializer
from Api.workforce.serializers import StaffSerializer


class OnCallSerializer(RepMixin, serializers.ModelSerializer):
    customer_data = CustomerSerializer(source='customer', read_only=True)
    category_data = CategorySerializer(source='category', read_only=True)
    service_data = ServiceSerializer(source='service', read_only=True)
    staffs_data = StaffSerializer(source='staffs', many=True, read_only=True)

    class Meta:
        model = OnCall
        fields = [
            'id','slug','date','status','type','customer','customer_data','category','category_data','service','service_data',
            'site_name','info','contact_person','contact_number','site_location','staffs','staffs_data'
        ]    