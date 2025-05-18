from django.urls import path
from Api.customers import views

app_name='api_customers'

urlpatterns=[
    path('customers/',views.CustomerListCreate.as_view(),name='customer_list_create'),
    path('customer/<slug:slug>/',views.CustomerDetails.as_view(),name='customer_details'),
]