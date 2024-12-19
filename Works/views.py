from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Works.models import Requisition, RequisitionItem, Work, Attendance
from Accounts.models import TransactionCategory, Transaction, Expense
from Technicians.models import Technician
from datetime import datetime
today = datetime.today()
from django.contrib import messages
from Customers.models import Lead

# Create your views here.

@login_required
def crete_requisition(request, slug):
    lead = Lead.objects.get(slug=slug)

    try:
        requisition = Requisition.objects.create(lead=lead, prepared=request.user)
    except Exception as exception:
        messages.error(request, exception)
        return redirect('lead-view', slug=lead.slug)

    return redirect('update-requisition', slug=requisition.slug)

@login_required
def requisition(request, slug):
    requisition = Requisition.objects.get(slug=slug)
    items = RequisitionItem.objects.filter(requisition=requisition).order_by('-id')

    context = {
        'main' : 'leads',
        'sub' : 'pending',
        'requisition' : requisition,
        'lead' : requisition.lead,
        'items' : items
    }
    return render(request,'requisition/requisition.html',context)

@login_required
def edit_requisition(request, slug):
    requisition = Requisition.objects.get(slug=slug)
    items = RequisitionItem.objects.filter(requisition=requisition).order_by('-id')

    context = {
        'main' : 'leads',
        'sub' : 'pending',
        'requisition' : requisition,
        'lead' : requisition.lead,
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
def works(request,status):
    works = Work.active_objects.filter(status=status.upper())
    context = {
        'main' : 'works',
        'sub' : status,
        'works' : works,
        'status' : status
    }
    return render(request,'works/works.html',context)

@user_passes_test(lambda u: u.is_superuser)
def work_details(request,slug):
    work = Work.objects.get(slug=slug)
    expenses = Expense.active_objects.filter(work=work)
    technicians = Technician.active_objects.all()
    attendances = Attendance.active_objects.filter(work=work,status=2)

    context = {
        'main' : 'works',
        'sub' : work.status.lower,
        'work' : work,
        'expenses' : expenses,
        'technicians' : technicians,
        'attendances' : attendances
    }
    return render(request,'works/work-details.html',context)

@user_passes_test(lambda u: u.is_superuser)
def assign_technician(request,slug):
    work = Work.objects.get(slug=slug)

    if request.method == 'POST':
        technicians = request.POST.getlist('technicians')
        work.technicians.set(technicians)

    return redirect('work-details',slug=work.slug)

@user_passes_test(lambda u: u.is_superuser)
def work_expense(request):
    categories = TransactionCategory.active_objects.filter(type='EXPENSE')
    works = Work.active_objects.all()

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

        return redirect('work-details',slug=work.slug)

    context = {
        'main' : 'works',
        'today' : today,
        'categories' : categories,
        'works' : works
    }
    return render(request,'works/work-expense.html',context)

@login_required
def assigned_works(request):

    context = {
        'main' : 'assigned-works',
    }

    return render(request,'technician/assigned-works.html', context)