from django.urls import path
from Works import views

urlpatterns = [
    path('list/<str:status>/',views.works,name='works'),
    path('view/<slug:slug>/',views.work_details,name='work-details'),
    path('assign/<slug:slug>/',views.assign_technician,name='assign-technician'),
    path('expenses/', views.work_expenses,name='work-expenses'),
    path('expense/add/',views.add_work_expense,name='add-work-expense'),
    path('expense/delete/<slug:slug>/',views.delete_work_expense,name='delete-work-expense'),

    #REQUISITION
    path('requisition/create/<slug:slug>/', views.crete_requisition,name='create-requisition'),
    path('requisition/<slug:slug>/', views.requisition, name='requisition'),
    path('requisition/update/<slug:slug>/', views.edit_requisition,name='update-requisition'),
    path('requisition/item/add/<slug:slug>/', views.add_requisition_item, name='add-requisition-item'),
    path('requisition/item/delete/<slug:slug>/', views.delete_requisition_item, name='delete-requisition-item'),

    # TECHNICIANS
    path('assigned-works/',views.assigned_works,name='assigned-works'),
]