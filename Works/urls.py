from django.urls import path
from Works import views

urlpatterns = [
    path('<str:status>/',views.works,name='works'),
    path('view/<slug:slug>/',views.work_details,name='work-details'),
]