from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Works.models import Requisition, RequisitionItem, Work, Attendance
from Accounts.models import TransactionCategory, Transaction, Expense
from Technicians.models import Technician
from datetime import datetime
today = datetime.today()
from django.contrib import messages
from Customers.models import Lead
from Works.models import Work
from django.db.models import Count,Sum

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
    expenses = Expense.active_objects.filter(work=work)
    technicians = Technician.active_objects.all()
    attendances = Attendance.active_objects.filter(work=work)
    requisitions = Requisition.active_objects.filter(work=work).annotate(items=Count('requisitionitem'))

    context = {
        'main' : 'works',
        'sub' : work.status.lower,
        'work' : work,
        'expenses' : expenses,
        'technicians' : technicians,
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
        technicians = request.POST.getlist('technicians')
        work.technicians.set(technicians)
        work.save()

    return redirect('work-details',slug=work.slug)

@login_required
def work_expenses(request):
    expenses = Expense.active_objects.filter(technician=request.user.technician).order_by('-id')
    self_expense = expenses.filter(source='SELF').aggregate(total=Sum('amount'))['total']
    petty_expense = expenses.filter(source='PETTY').aggregate(total=Sum('amount'))['total']
    credit_expense = expenses.filter(source='CREDIT').aggregate(total=Sum('amount'))['total']
    petty_balance = 0.0
    
    context = {
       'main' : 'accounts',
       'sub' : 'work-expenses',
       'expenses' : expenses,
       'self_expense' : self_expense,
       'petty_expense' : petty_expense,
       'credit_expense' : credit_expense,
       'petty_balance' : petty_balance
    }

    return render(request, 'accounts/work-expenses.html', context)

@login_required
def add_work_expense(request):
    categories = TransactionCategory.active_objects.filter(type='EXPENSE')
    works = Work.active_objects.filter(technicians__in=[request.user.technician])

    if request.method == 'POST':
        date = request.POST.get('date')
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        source = request.POST.get('source')
        amount = request.POST.get('amount')
        work = request.POST.get('work')

        try:
            category = TransactionCategory.objects.get(slug=category)
            work = Work.objects.get(slug=work)

            try:
                technician = Technician.objects.get(user=request.user)
            except Technician.DoesNotExist:
                technician = None

            Expense.objects.create(
                date=date, work=work, technician=technician, category=category,
                title=title, description=description, source=source, amount=amount
            )
            messages.success(request,'Expense added successfully')

        except Exception as exception:
            messages.warning(request,exception)

        return redirect('work-expenses')

    context = {
        'main' : 'works',
        'today' : today,
        'categories' : categories,
        'works' : works
    }
    return render(request,'works/work-expense.html',context)

@login_required
def delete_work_expense(request, slug):
    try:
        expense = Expense.objects.get(slug=slug)
        expense.delete()
        messages.success(request,'Expense deleted successfully')
        return redirect('work-expenses')

    except Exception as exception:
        messages.warning(request,str(exception))
        return redirect('work-expenses')


@login_required
def assigned_works(request):
    if hasattr(request.user, 'technician') and request.user.technician:
        sites = Lead.active_objects.filter(staffs__in=[request.user.technician], status="PENDING")
        works = Work.active_objects.filter(technicians__in=[request.user.technician])
    else:
        sites = []
        works = []

    context = {
        'main': 'assigned-works',
        'sites': sites,
        'works': works,
    }

    return render(request, 'technician/assigned-works.html', context)