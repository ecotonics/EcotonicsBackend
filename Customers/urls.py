from django.urls import path
from Customers import views

urlpatterns = [
    #CUSTOMERS
    path('customers/<str:type>/',views.customers,name='customers'),
    path('customer/add/<str:type>/',views.add_customer,name='customer-add'),
    path('customer/edit/<slug:slug>/',views.edit_customer,name='customer-edit'),
    path('customer/details/<slug:slug>/',views.customer_details,name='customer-details'),
    path('customer/delete/<slug:slug>/',views.delete_customer,name='customer-delete'),
    path('filter-customers/',views.filter_customers,name='filter-customers'),
]