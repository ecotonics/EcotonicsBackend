from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from Workforce.models import Department, Designation, Staff
from Users.models import User

from Api.workforce.serializers import DepartmentSerializer, DesignationSerializer, StaffSerializer, UserSerializer
from Api.workforce.filters import DepartmentFilter, DesignationFilter, StaffFilter


class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {
            "departments": serializer.data,
        }

        return Response({
            'status': 'success',
            'message': 'Departments retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Department created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create department',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Department retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Department updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update department',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Department deleted successfully'
        }, status=status.HTTP_200_OK)
    

class DesignationListCreate(generics.ListCreateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DesignationFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {
            "designations": serializer.data,
        }

        return Response({
            'status': 'success',
            'message': 'Designations retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Designation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'error',
            'message': 'Failed to create designation',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DesignationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Designation retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Designation updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update designation',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Designation deleted successfully'
        }, status=status.HTTP_200_OK)
    

class StaffListCreate(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StaffFilter
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})

        data = {
            "staffs": serializer.data,
        }

        return Response({
            'status': 'success',
            'message': 'Staffs retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            user_serializer = UserSerializer(data=request.data, context={'request': request})
            if not user_serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Failed to create user',
                    'errors': user_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            user = user_serializer.save()

            staff_data = request.data.copy()
            staff_data['user'] = user.id

            staff_serializer = self.get_serializer(data=staff_data, context={'request': request})
            if not staff_serializer.is_valid():
                user.delete()
                return Response({
                    'status': 'error',
                    'message': 'Failed to create staff',
                    'errors': staff_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            staff = staff_serializer.save()

            return Response({
                'status': 'success',
                'message': 'Staff created successfully',
                'data': staff_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An error occurred: {str(e)}',
                'errors': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StaffDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'status': 'success',
            'message': 'Staff retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Staff updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Failed to update staff',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            'status': 'success',
            'message': 'Designation deleted successfully'
        }, status=status.HTTP_200_OK)