from django.urls import path
from Works import views

urlpatterns = [
    path('list/<str:status>/',views.works,name='works'),
    path('view/<slug:slug>/',views.work_details,name='work-details'),
    path('assign/<slug:slug>/',views.assign_technician,name='assign-technician'),

    #REQUISITION
    path('requisition/create/<slug:slug>/', views.crete_requisition,name='create-requisition'),
    path('requisition/<slug:slug>/', views.requisition, name='requisition'),
    path('requisition/update/<slug:slug>/', views.edit_requisition,name='update-requisition'),
    path('requisition/item/add/<slug:slug>/', views.add_requisition_item, name='add-requisition-item'),
    path('requisition/item/delete/<slug:slug>/', views.delete_requisition_item, name='delete-requisition-item'),

    # TECHNICIANS
    path('assigned-works/',views.assigned_works,name='assigned-works'),

    # SERVICE CALLS
    path('on-calls/',views.on_calls, name='on-calls'),
    path('on-call/add/',views.add_on_call, name='on-call-add'),
    path('on-call/details/<slug:slug>/',views.on_call_details, name='on-call-details'),
    path('on-call/edit/<slug:slug>/', views.edit_on_call, name='on-call-edit'),
    path('on-call/staff/assign/<slug:slug>/',views.assign_on_call_technician,name='assign-on-call-technician'),
    path('on-call/expense/add/<slug:slug>/',views.add_on_call_expense,name='add-on-call-expense'),
    path('on-call/expense/delete/<slug:slug>/',views.delete_on_call_expense,name='delete-on-call-expense'),
]