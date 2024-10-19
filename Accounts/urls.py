from django.urls import path
from Accounts import views

urlpatterns = [
    path('transaction/categories/', views.transaction_categories, name='transaction-categories'),
    path('transaction/categories/add/', views.add_transaction_category, name='transaction-category-add'),
    path('transaction/categories/edit/<slug:slug>/', views.edit_transaction_category, name='transaction-category-edit'),

    path('banks/',views.bank_accounts,name='bank-accounts'),
    path('bank/add/',views.add_bank_account,name='bank-account-add'),
    path('bank/edit/<slug:slug>/',views.edit_bank_account,name='bank-account-edit'),
]
