from django.urls import path
from Accounts import views

urlpatterns = [
    path('accounts/transaction/categories/', views.transaction_categories, name='transaction-categories'),
    path('accounts/transaction/categories/add/', views.add_transaction_category, name='transaction-category-add'),
    path('accounts/transaction/categories/edit/<slug:slug>/', views.edit_transaction_category, name='transaction-category-edit'),
]
