from Services.models import Category, Service
from Works.models import OnCall
from rest_framework import serializers
from Core.mixins import RepMixin

class CategorySerializer(RepMixin, serializers.ModelSerializer):
    services = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id','slug','name','status','info','services']

    def get_services(self, category):
        services = Service.objects.filter(category=category).count()
        return services


class ServiceSerializer(RepMixin, serializers.ModelSerializer):
    category_data = CategorySerializer(read_only=True)
    on_calls = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id','slug','name','status','category','category_data', 'info', 'on_calls']

    def get_on_calls(self, service):
        on_calls = OnCall.objects.filter(service=service).count()
        return on_calls

