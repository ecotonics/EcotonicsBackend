from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Works.models import Requisition, RequisitionItem, Work, Attendance
from Accounts.models import TransactionCategory, Transaction, BankAccount
from Workforce.models import Staff
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
    else:
        sites = []
        works = []

    context = {
        'main': 'assigned-works',
        'sites': sites,
        'works': works,
    }

    return render(request, 'technician/assigned-works.html', context)