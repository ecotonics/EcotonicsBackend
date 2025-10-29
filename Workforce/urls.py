from django.urls import path
from Workforce import views

urlpatterns = [
    # DEPARTMENTS
    path('departments/', views.departments, name='departments'),
    path('department/add/', views.add_department, name='department-add'),
    path('department/edit/<slug:slug>/', views.edit_department, name='department-edit'),
    path('department/detail/<slug:slug>/', views.department_details, name='department-details'),
    path('department/delete/<slug:slug>/', views.delete_department, name='department-delete'),

    # DESIGNATIONS
    path('designation/', views.designations, name='designations'),
    path('designation/add/', views.add_designation, name='designation-add'),
    path('designation/edit/<slug:slug>/', views.edit_designation, name='designation-edit'),
    path('designation/detail/<slug:slug>/', views.designation_details, name='designation-details'),
    path('designation/delete/<slug:slug>/', views.delete_designation, name='designation-delete'),

    # TECHNICIANS
    path('staffs/',views.staffs,name='staffs'),
    path('staff/add/',views.add_staff,name='staff-add'),
    path('staff/edit/<slug:slug>/',views.edit_staff,name='staff-edit'),
    path('staff/details/<slug:slug>/',views.staff_details,name='staff-details'),
    path('staff/delete/<slug:slug>/',views.delete_staff,name='staff-delete'),

    # ATTANDENCE
    path('attendance/add/<slug:slug>/',views.add_attandance,name='attendance-add'),
    path('attendance/edit/<slug:slug>/',views.edit_attandance,name='attendance-edit'),
    path('attendance/delete/<slug:slug>/',views.delete_attandance,name='attendance-delete'),

    # WAGES
    path('wage/update/<slug:slug>/',views.update_wage,name='wage-update'),
    path('wage/delete/<slug:slug>/',views.delete_wage,name='wage-delete'),
    path('wage/pay/<slug:slug>/', views.pay_wage, name='pay-wage'),

    # PAYMENTS
    path('payment/add/<slug:slug>/',views.add_payment,name='payment-add'),
    path('payment/mark/payed/<slug:slug>/',views.mark_paid,name='mark-payed'),
    path('payment/delete/<slug:slug>/',views.delete_payment,name='payment-delete')
]