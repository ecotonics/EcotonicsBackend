from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Accounts.models import TransactionCategory
from django.contrib import messages

# Create your views here.

@login_required
def transaction_categories(request):
    categories = TransactionCategory.active_objects.all()

    context = {
        'main' : 'accounts',
        'sub' : 'categories',
        'categories' : categories
    }

    return render(request,'accounts/categories.html',context)

@login_required
def add_transaction_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        info = request.POST.get('info')

        try:
            TransactionCategory.objects.create(name=name,info=info)
            messages.success(request,'Transaction category added successfully ... !')
            return redirect('transaction-categories')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('transaction-category-add')

    context = {
        'main' : 'accounts',
        'sub' : 'categories',
    }

    return render(request,'accounts/category-add.html',context)

@login_required
def edit_transaction_category(request,slug):
    category = TransactionCategory.objects.get(slug=slug)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.info = request.POST.get('info')

        try:
            category.save()
            messages.success(request,'Transaction category edited successfully ... !')
            return redirect('transaction-categories')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('transaction-category-add')

    context = {
        'main' : 'accounts',
        'sub' : 'categories',
        'category' : category
    }

    return render(request,'accounts/category-edit.html',context)