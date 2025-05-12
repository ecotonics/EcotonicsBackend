from django.urls import path
from Api.services import views

app_name='api_service'

urlpatterns=[
    path('categories/',views.CategoryListCreate.as_view(),name='category_list_create'),
    path('category/<slug:slug>/',views.CategoryDetails.as_view(),name='category_details'),

    path('services/',views.ServiceListCreate.as_view(),name='service_list_create'),
    path('service/<slug:slug>/',views.ServiceDetails.as_view(),name='service_details'),
]