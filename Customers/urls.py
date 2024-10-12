from django.urls import path
from Customers import views

urlpatterns = [
    #CUSTOMERS
    path('customers/enterprises/',views.enterprises,name='enterprises'),
    path('customers/intivituals/',views.intividuals,name='intividuals'),
    path('customer/add/',views.add_customer,name='customer-add'),
    path('customer/edit/',views.edit_customer,name='customer-edit'),
    path('customer/delete/',views.delete_customer,name='customer-delete'),

    #LEADS
    path('leads/intivituals/',views.leads,name='leads'),
    path('lead/add/',views.add_lead,name='lead-add'),
    path('lead/edit/',views.edit_lead,name='lead-edit'),
    path('lead/delete/',views.delete_lead,name='lead-delete'),
]