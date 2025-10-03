from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Works.models import Attendance
from Accounts.models import TransactionCategory, Transaction, BankAccount
from Workforce.models import Staff
from datetime import datetime
from django.contrib import messages
from Customers.models import Customer
from Works.models import OnCall, Task
from Services.models import Category, Service
from django.db.models import Count,Sum

today = datetime.today()

# Create your views here.

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
    staffs = Staff.active_objects.filter(status='active')
    categories = TransactionCategory.active_objects.filter(type='EXPENSE')
    transactions = Transaction.active_objects.filter(on_call=on_call)

    revanue_amount = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense_amount = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    net_amount = float(revanue_amount) - float(expense_amount)

    attendances = Attendance.active_objects.filter(on_call=on_call)
    attendance_summary = (
        attendances.values("staff__id", "staff__user__first_name", "staff__user__last_name")
        .annotate(total_days=Count("date", distinct=True))
        .order_by("-total_days")
    )

    context = {
        'main' : 'calls',
        'on_call' : on_call,
        'staffs' : staffs,
        'categories' : categories,
        'transactions' : transactions,
        'revanue_amount' : revanue_amount,
        'expense_amount' : expense_amount,
        'net_amount' : net_amount,
        'attendances' : attendances,
        'attendance_summary' : attendance_summary
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
        on_call.status = 'ongoing'
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

            Transaction.objects.create(
                date=today, category=category, type=category.type, customer=on_call.customer, on_call=on_call, title=title, amount=amount
            )

            messages.success(request, 'work transaction added')
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


@user_passes_test(lambda u: u.is_superuser)
def complete_on_call(request, slug):
    on_call = OnCall.active_objects.filter(slug=slug).first()
    on_call.status = 'completed'
    on_call.save()
    return redirect('on-call-details', slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def tasks(request):
    tasks = Task.active_objects.all()

    context = {
        'main' : 'tasks',
        'tasks' : tasks
    }
    return render(request,'tasks/tasks.html',context)


@user_passes_test(lambda u: u.is_superuser)
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')

        try:
            Task.objects.create(
                date=date, title=title, description=description
            )

            messages.success(request,'Task addedd successfully')
            return redirect('tasks')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('task-add')

    context = {
        'main' : 'tasks',
        'today' : today
    }
    return render(request,'tasks/task-add.html',context)


@user_passes_test(lambda u: u.is_superuser)
def edit_task(request,slug):
    task = Task.active_objects.filter(slug=slug).first()

    if request.method == 'POST':
        date = request.POST.get('date')
        title = request.POST.get('title')
        description = request.POST.get('description')

        try:
            task.date = date
            task.title = title
            task.description = description
            task.save()

            messages.success(request,'Task updated successfully')
            return redirect('tasks')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('task-edit', slug=slug)

    context = {
        'main' : 'tasks',
        'task' : task,
        'today' : today
    }
    return render(request,'tasks/task-edit.html',context)


@user_passes_test(lambda u: u.is_superuser)
def delete_task(request, slug):
    try:
        task = Task.active_objects.filter(slug=slug).first()
        task.is_deleted = True
        task.save()

        messages.success(request, 'Task deleted')
    except Exception as exception:
        messages.warning(request, str(exception))

    return redirect('tasks')


@user_passes_test(lambda u: u.is_superuser)
def complete_task(request, slug):
    task = Task.active_objects.filter(slug=slug).first()
    task.is_completed = True
    task.save()
    return redirect('tasks')