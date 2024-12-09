from django.urls import path
from Services import views

urlpatterns = [
    # SERVICE CATEGORY
    path('categories/',views.categories,name='categories'),
    path('category/add/',views.add_category,name='category-add'),
    path('category/details/<slug:slug>/',views.category_details,name='category-details'),
    path('category/edit/<slug:slug>/',views.edit_category,name='category-edit'),
    path('category/delete/<slug:slug>/',views.delete_category,name='category-delete'),

    # SERVICE
    path('services/',views.services,name='services'),
    path('service/add/',views.add_service,name='service-add'),
    path('service/edit/<slug:slug>/',views.edit_service,name='service-edit'),
    path('service/delete/<slug:slug>/',views.delete_service,name='service-delete'),
    path('service/details/<slug:slug>/',views.service_details,name='service-details'),

    # SERVICE CALLS
    path('calls/',views.calls,name='calls'),
    path('call/add/',views.add_call,name='call-add'),

    path('filter-service/',views.filter_service,name='filter-service')
]