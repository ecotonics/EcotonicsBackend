from Customers.models import Customer
from Api.customers.serializers import CustomerSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from Api.customers.filters import CustomerFilter


class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {
            "customers": serializer.data,
            "total_customers": Customer.objects.count(),
            "individual_customers": Customer.objects.filter(type="individual").count(),
            "enterprise_customers": Customer.objects.filter(type="enterprise").count(),
        }

        return Response({
            'status': 'success',
            'message': 'Customers retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Customer created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create customer',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Customer retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Customer updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update customer',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Customer deleted successfully'
        }, status=status.HTTP_200_OK)