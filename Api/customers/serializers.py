from Customers.models import Customer
from rest_framework import serializers
from Core.mixins import RepMixin

class CustomerSerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id','slug','status','name','location','mobile','email','type']