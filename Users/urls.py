from django.urls import path
from Users import views

urlpatterns = [
    path('sign-in',views.sign_in,name='sign-in'),
    path('sign-out',views.signout,name='sign-out')
]