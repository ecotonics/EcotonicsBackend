from django.urls import path
from Api.workforce import views

app_name='api_workforce'

urlpatterns=[
    path('departments/',views.DepartmentListCreate.as_view(),name='department_list_create'),
    path('department/<slug:slug>/',views.DepartmentDetails.as_view(),name='department_details'),

    path('designations/',views.DesignationListCreate.as_view(),name='designation_list_create'),
    path('designation/<slug:slug>/',views.DesignationDetails.as_view(),name='designation_details'),
]