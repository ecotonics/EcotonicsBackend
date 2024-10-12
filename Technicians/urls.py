from django.urls import path
from Technicians import views

urlpatterns = [
    # TECHNICIANS
    path('technicians/',views.technicians,name='technicians'),
    path('technician/add/',views.add_technician,name='technician-add'),
    path('technician/edit/',views.edit_technician,name='technician-edit'),
    path('technician/details/',views.technician_details,name='technician-details'),
    path('technician/delete/',views.delete_technician,name='technician-delete'),

    # ATTANDENCE
    path('attandance/',views.attandance,name='attandance'),
    path('attandance/add/',views.add_attandance,name='attandance-add'),
    path('attandance/edit/',views.edit_attandance,name='attandance-edit'),
    path('attandance/delete/',views.delete_attandance,name='attandance-delete'),
]