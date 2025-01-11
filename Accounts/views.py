from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Accounts.models import TransactionCategory, BankAccount, Transaction
from django.contrib import messages
from datetime import datetime
today = datetime.today()
from django.http import JsonResponse
from django.db.models import Sum
from Customers.models import Customer, Lead
from Works.models import Work
from Workforce.models import Staff

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def overview(request):
    transactions = Transaction.active_objects.all()[:10]
    total_income = Transaction.active_objects.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.active_objects.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'main' : 'accounts',
        'sub' : 'overview',
        'transactions' : transactions,
        'total_income' : float(total_income),
        'total_expense' : float(total_expense),
        'balance' : float(balance)
    }

    return render(request,'accounts/overview.html',context)

@user_passes_test(lambda u: u.is_superuser)
def transaction_categories(request):
    categories = TransactionCategory.active_objects.all()

    context = {
        'main' : 'accounts',
        'sub' : 'categories',
        'categories' : categories
    }

    return render(request,'accounts/categories.html',context)

@user_passes_test(lambda u: u.is_superuser)
def add_transaction_category(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        name = request.POST.get('name')
        info = request.POST.get('info')

        try:
            TransactionCategory.objects.create(type=type,name=name,info=info)
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

@user_passes_test(lambda u: u.is_superuser)
def edit_transaction_category(request,slug):
    category = TransactionCategory.objects.get(slug=slug)

    if request.method == 'POST':
        category.type = request.POST.get('type')
        category.name = request.POST.get('name')
        category.info = request.POST.get('info')

        try:
            category.save()
            messages.success(request,'Transaction category edited successfully ... !')
            return redirect('transaction-categories')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('transaction-category-edit',slug=category.slug)

    context = {
        'main' : 'accounts',
        'sub' : 'categories',
        'category' : category
    }

    return render(request,'accounts/category-edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def bank_accounts(request):
    accounts = BankAccount.active_objects.all()
    context = {
        'main' : 'accounts',
        'sub' : 'bank-accounts',
        'accounts' : accounts
    }
    return render(request,'accounts/bank-accounts.html',context)

@user_passes_test(lambda u: u.is_superuser)
def add_bank_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        number = request.POST.get('number')
        branch = request.POST.get('branch')

        try:
            BankAccount.objects.create(name=name,account=account,number=number,branch=branch)
            messages.success(request,'Bank account added successfully ... !')
            return redirect('bank-accounts')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('bank-account-add')

    context = {
        'main' : 'accounts',
        'sub' : 'bank-accounts',
    }

    return render(request,'accounts/bank-account-add.html',context)

@user_passes_test(lambda u: u.is_superuser)
def edit_bank_account(request,slug):
    account = BankAccount.objects.get(slug=slug)
    if request.method == 'POST':
        account.name = request.POST.get('name')
        account.account = request.POST.get('account')
        account.number = request.POST.get('number')
        account.branch = request.POST.get('branch')

        try:
            account.save()
            messages.success(request,'Bank account detail edited successfully ... !')
            return redirect('bank-accounts')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('bank-account-edit',slug=account.slug)

    context = {
        'main' : 'accounts',
        'sub' : 'bank-accounts',
        'account' : account
    }

    return render(request,'accounts/bank-account-edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def transactions(request):
    transactions = Transaction.active_objects.all()
    context = {
        'main' : 'accounts',
        'sub' : 'transactions',
        'transactions' : transactions
    }
    return render(request,'accounts/transactions.html',context)

def filter_category(request):
    type = request.GET.get('type')
    category_list = TransactionCategory.active_objects.filter(type=type).values('slug', 'name')
    category_data = list(category_list)

    return JsonResponse({'categories': category_data})

@user_passes_test(lambda u: u.is_superuser)
def add_transaction(request):
    accounts = BankAccount.active_objects.all()
    if request.method == 'POST':
        date = request.POST.get('date')
        category = request.POST.get('category')
        title = request.POST.get('title')
        account = request.POST.get('account')
        amount = request.POST.get('amount')

        try:
            category = TransactionCategory.active_objects.get(slug=category)
            account = BankAccount.active_objects.get(slug=account)

            Transaction.objects.create(date=date,category=category,type=category.type,title=title,account=account,amount=amount)
            messages.success(request,'Transaction added successfully ... !')
            return redirect('transactions')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('transaction-add')

    context = {
        'main' : 'accounts',
        'sub' : 'transactions',
        'today' : today,
        'accounts' : accounts
    }

    return render(request,'accounts/transaction-add.html',context)

@user_passes_test(lambda u: u.is_superuser)
def edit_transaction(request,slug):
    accounts = BankAccount.active_objects.all()
    transaction = Transaction.objects.get(slug=slug)
    categories = TransactionCategory.objects.filter(type = transaction.type)
    if request.method == 'POST':
        transaction.date = request.POST.get('date')
        transaction.title = request.POST.get('title')
        transaction.amount = request.POST.get('amount')

        category = request.POST.get('category')
        account = request.POST.get('account')

        try:
            category = TransactionCategory.active_objects.get(slug=category)
            account = BankAccount.active_objects.get(slug=account)

            transaction.save()
            messages.success(request,'Transaction details edited successfully ... !')
            return redirect('transactions')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('transaction-edit',slug=slug)

    context = {
        'main' : 'accounts',
        'sub' : 'transactions',
        'transaction' : transaction,
        'today' : today,
        'categories' : categories,
        'accounts' : accounts,
    }
    return render(request,'accounts/transaction-edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def delete_transaction(request,slug):
    try:
        transaction = Transaction.objects.get(slug=slug)
        transaction.is_deleted = True
        transaction.save()
        messages.warning(request,'Transaction deleted successfully ...!')
    except Exception as exception:
        messages.warning(request,str(exception))
    return redirect('transactions')


@user_passes_test(lambda u: u.is_superuser)
def add_expense(request):
    date = request.POST.get('date')

    lead = request.POST.get('lead') or None
    work = request.POST.get('work') or None
    customer = request.POST.get('customer') or None
    staff = request.POST.get('staff') or None
    category = request.POST.get('category') or None

    title = request.POST.get('title')
    account = request.POST.get('account')
    amount = request.POST.get('amount')

    page = request.POST.get('page')
    
    if lead:
        lead = Lead.objects.get(slug=lead)
    
    if work:
        work = Work.objects.get(slug=work)

    if customer:
        customer = Customer.objects.get(slug=customer)

    if staff:
        staff = Staff.objects.get(slug=staff)

    if category:
        category = TransactionCategory.objects.get(slug=category)

    if account:
        account = BankAccount.objects.get(slug=account)

    try:
        Transaction.objects.create(
            date=date, lead=lead, work=work, customer=customer, staff=staff, category=category, type=category.type, title=title, account=account, amount=amount
        )
        messages.success(request, 'Expense added')

    except Exception as exception:
        messages.warning(request, exception)

    if page == 'lead':
        return redirect('lead-view', slug=lead.slug)
    elif page == 'work':
        return request('work-details', slug=work.slug)