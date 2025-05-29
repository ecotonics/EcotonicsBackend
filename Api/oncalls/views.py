from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from Works.models import OnCall
from Customers.models import Customer
from Api.oncalls.serializers import OnCallSerializer
from Api.oncalls.filters import OnCallFilter


class OnCallListCreate(generics.ListCreateAPIView):
    queryset = OnCall.objects.all()
    serializer_class = OnCallSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OnCallFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {
            "on_calls": serializer.data,
            "total_on_calls": OnCall.objects.count(),
            "pending_on_calls": OnCall.objects.filter(status="Pending").count(),
            "ongoing_on_calls": OnCall.objects.filter(status="Ongoing").count(),
            "completed_on_calls": OnCall.objects.filter(status="Completed").count(),
            "cancelled_on_calls": OnCall.objects.filter(status="Cancelled").count(),
        }

        return Response({
            'status': 'success',
            'message': 'On Calls retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not request.data['customer']:
                customer = Customer.objects.create(
                    name=request.data['name'],
                    mobile=request.data['mobile'],
                    email=request.data['email']
                )

            if request.data['customer']:
                customer = Customer.objects.get(id=request.data['customer'])

            serializer.save(customer=customer)

            return Response({
                'status': 'success',
                'message': 'On Call created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create on call',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OnCallDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = OnCall.objects.all()
    serializer_class = OnCallSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'On Call retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'On Call updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update on call',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'On Call deleted successfully'
        }, status=status.HTTP_200_OK)