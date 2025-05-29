from django.urls import path
from Api.oncalls import views

app_name='api_oncall'

urlpatterns=[
    path('oncalls/',views.OnCallListCreate.as_view(),name='oncall_list_create'),
    path('oncall/<slug:slug>/',views.OnCallDetails.as_view(),name='oncall_details'),
]