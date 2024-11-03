from django.urls import path
from Customers import views

urlpatterns = [
    #CUSTOMERS
    path('customers/<str:type>/',views.customers,name='customers'),
    path('customer/add/<str:type>/',views.add_customer,name='customer-add'),
    path('customer/edit/<slug:slug>/',views.edit_customer,name='customer-edit'),
    path('customer/delete/<slug:slug>/',views.delete_customer,name='customer-delete'),

    #LEADS
    path('leads/<str:status>/',views.leads,name='leads'),
    path('lead/add/',views.add_lead,name='lead-add'),
    path('lead/details/<slug:slug>/',views.view_lead,name='lead-view'),
    path('lead/edit/<slug:slug>/',views.edit_lead,name='lead-edit'),
    path('lead/delete/<slug:slug>/',views.delete_lead,name='lead-delete'),
    path('lead/convert/<slug:slug>/',views.convert_lead,name='lead-convert'),

    #FOLLOWUP
    path('followup/<slug:slug>/',views.followup,name='followup')
]