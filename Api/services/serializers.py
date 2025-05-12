from Services.models import Category, Service
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
    class Meta:
        model = Service
        fields = ['id','slug','name','status','category','info']

