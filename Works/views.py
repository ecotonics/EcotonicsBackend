from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Works.models import Requisition, RequisitionItem, Work, Attendance
from Accounts.models import TransactionCategory, Transaction, BankAccount
from Workforce.models import Staff
from datetime import datetime
from django.contrib import messages
from Customers.models import Lead, Customer
from Works.models import Work, OnCall
from Services.models import Category, Service
from django.db.models import Count,Sum

today = datetime.today()

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def works(request,status):
    works = Work.active_objects.filter(status=status.upper())
    context = {
        'main' : 'works',
        'sub' : status,
        'works' : works,
        'status' : status
    }
    return render(request,'works/works.html',context)

@login_required
def work_details(request,slug):
    work = Work.objects.get(slug=slug)
    transactions = Transaction.active_objects.filter(work=work)
    staffs = Staff.active_objects.all()
    attendances = Attendance.active_objects.filter(work=work)
    requisitions = Requisition.active_objects.filter(work=work).annotate(items=Count('requisitionitem'))
    accounts = BankAccount.active_objects.all()

    context = {
        'main' : 'works',
        'sub' : work.status.lower,
        'work' : work,
        'transactions' : transactions,
        'staffs' : staffs,
        'accounts' : accounts,
        'attendances' : attendances,
        'requisitions' : requisitions
    }
    return render(request,'works/work-details.html',context)

@login_required
def crete_requisition(request, slug):
    work = Work.objects.get(slug=slug)

    try:
        requisition = Requisition.objects.create(work=work, prepared=request.user)
    except Exception as exception:
        messages.error(request, exception)
        return redirect('work-details', slug=work.slug)

    return redirect('update-requisition', slug=requisition.slug)

@login_required
def requisition(request, slug):
    requisition = Requisition.objects.get(slug=slug)
    items = RequisitionItem.objects.filter(requisition=requisition).order_by('-id')

    context = {
        'main' : 'works',
        'sub' : requisition.work.status.lower(),
        'requisition' : requisition,
        'work' : requisition.work,
        'items' : items
    }
    return render(request,'requisition/requisition.html',context)

@login_required
def edit_requisition(request, slug):
    requisition = Requisition.objects.get(slug=slug)
    items = RequisitionItem.objects.filter(requisition=requisition).order_by('-id')

    context = {
        'main' : 'works',
        'sub' : requisition.work.status.lower(),
        'requisition' : requisition,
        'work' : requisition.work,
        'items' : items
    }
    return render(request,'requisition/requisition-update.html',context)

@login_required
def add_requisition_item(request, slug):
    requisition = Requisition.objects.get(slug=slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        quantity = request.POST.get('quantity')

        try:
            RequisitionItem.objects.create(requisition=requisition, name=name, unit=unit, quantity=quantity)
            messages.success(request,'Item added successfully...')
        except Exception as exception:
            messages.warning(request,str(exception))

    return redirect('update-requisition', slug=slug)

@login_required
def delete_requisition_item(request, slug):
    item = RequisitionItem.objects.get(slug=slug)
    requisition = item.requisition
    item.delete()
    messages.success(request,'Item deleted successfully...')
    
    return redirect('update-requisition', slug=requisition.slug)

@user_passes_test(lambda u: u.is_superuser)
def assign_technician(request,slug):
    work = Work.objects.get(slug=slug)

    if request.method == 'POST':
        staffs = request.POST.getlist('staffs')
        work.staffs.set(staffs)
        work.save()

    return redirect('work-details',slug=work.slug)


@login_required
def assigned_works(request):
    if hasattr(request.user, 'staff') and request.user.staff:
        sites = Lead.active_objects.filter(staffs__in=[request.user.staff], status="PENDING")
        works = Work.active_objects.filter(staffs__in=[request.user.staff])
        on_calls = OnCall.active_objects.filter(staffs__in=[request.user.staff])
    else:
        sites = []
        works = []
        on_calls = []

    context = {
        'main': 'assigned-works',
        'sites': sites,
        'works': works,
        'on_calls' : on_calls
    }

    return render(request, 'technician/assigned-works.html', context)


@user_passes_test(lambda u: u.is_superuser)
def on_calls(request):
    on_calls = OnCall.active_objects.all()

    context = {
        'main' : 'calls',
        'on_calls' : on_calls
    }
    return render(request,'oncalls/calls.html',context)

@user_passes_test(lambda u: u.is_superuser)
def add_on_call(request):
    categories = Category.active_objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        category = request.POST.get('category')
        service = request.POST.get('service')
        info = request.POST.get('info')
        on_call_type = request.POST.get('lead_type')
        work_type = request.POST.get('work_type')
        customer = request.POST.get('customer')
        site_name = request.POST.get('site_name')

        try:
            category = Category.objects.get(slug=category)
            service = Service.objects.get(slug=service)

            if on_call_type == 'new':
                customer = Customer.objects.create(type=work_type, name=name, location=location, mobile=mobile, email=email)

            elif on_call_type == 'existing':
                customer = Customer.objects.get(slug=customer)

            OnCall.objects.create(
                type=work_type, category=category, service=service, info=info, customer=customer, site_name=site_name
            )

            messages.success(request,'On call addedd successfully')
            return redirect('on-calls')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('on-call-add')

    context = {
        'main' : 'calls',
        'categories' : categories
    }
    return render(request,'oncalls/call-add.html',context)


def on_call_details(request, slug):
    on_call = OnCall.active_objects.filter(slug=slug).first()
    staffs = Staff.active_objects.all()
    categories = TransactionCategory.active_objects.filter(type='EXPENSE')
    expenses = Transaction.active_objects.filter(on_call=on_call)
    expense_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'main' : 'calls',
        'on_call' : on_call,
        'staffs' : staffs,
        'categories' : categories,
        'expenses' : expenses,
        'expense_amount' : expense_amount
    }
    return render(request, 'oncalls/call-details.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_on_call(request,slug):
    on_call = OnCall.active_objects.filter(slug=slug).first()
    categories = Category.active_objects.all()
    customers = Customer.active_objects.all()
    services = Service.active_objects.filter(category=on_call.category)

    if request.method == 'POST':
        customer = request.POST.get('customer')
        site_name = request.POST.get('site_name')
        category = request.POST.get('category')
        service = request.POST.get('service')
        info = request.POST.get('info')

        try:
            customer = Customer.objects.get(slug=customer)
            category = Category.objects.get(slug=category)
            service = Service.objects.get(slug=service)

            on_call.customer = customer
            on_call.category = category
            on_call.service = service
            on_call.site_name = site_name
            on_call.info = info
            
            on_call.save()

            messages.success(request,'On call updated successfully')
            return redirect('on-calls')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('on-call-edit', slug=slug)

    context = {
        'main' : 'calls',
        'on_call' : on_call,
        'categories' : categories,
        'customers' : customers,
        'services' : services
    }
    return render(request,'oncalls/call-edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def assign_on_call_technician(request,slug):
    on_call = OnCall.objects.get(slug=slug)

    if request.method == 'POST':
        staffs = request.POST.getlist('staffs')
        on_call.staffs.set(staffs)
        on_call.save()

    return redirect('on-call-details',slug=on_call.slug)


@login_required
def add_on_call_expense(request, slug):
    on_call = OnCall.active_objects.filter(slug=slug).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_slug = request.POST.get('category')

        try:
            category = TransactionCategory.objects.get(slug=category_slug)

            if not request.user.is_superuser:
                staff = request.user.staff
            else:
                staff = None

            Transaction.objects.create(
                date=today, category=category, type=category.type, customer=on_call.customer, on_call=on_call, staff=staff, title=title, amount=amount
            )

            messages.success(request, 'work expense added')
            return redirect('on-call-details', slug=slug)
        
        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('on-call-details', slug=slug)
        
@login_required
def delete_on_call_expense(request, slug):
    try:
        expense = Transaction.active_objects.filter(slug=slug).first()
        expense.is_deleted = True
        expense.save()

        messages.success(request, 'On call expense deleted')
    except Exception as exception:
        messages.warning(request, str(exception))

    return redirect('on-call-details', slug=expense.on_call.slug)