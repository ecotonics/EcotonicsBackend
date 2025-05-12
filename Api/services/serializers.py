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
        return Service.objects.filter(category=category).count()


class ServiceSerializer(RepMixin, serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    on_calls = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id','slug','name','status','category','category_name', 'category_id', 'info', 'on_calls']

    def get_category_name(self, service):
        return service.category.name

    def get_category_id(self, service):
        return service.category.id

    def get_on_calls(self, service):
        return OnCall.objects.filter(service=service).count()

