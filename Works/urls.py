from django.urls import path
from Works import views

urlpatterns = [
    path('<str:status>/',views.works,name='works'),
    path('view/<slug:slug>/',views.work_details,name='work-details'),
    path('assign/<slug:slug>/',views.assign_technician,name='assign-technician'),
    path('expense/list/',views.work_expense,name='work-expenses'),
]