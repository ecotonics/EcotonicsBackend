from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Works.models import Work, Attendance
from Accounts.models import TransactionCategory, Transaction, Expense
from Technicians.models import Technician
from datetime import datetime
today = datetime.today()
from django.contrib import messages

# Create your views here.

@login_required
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

@login_required
def assign_technician(request,slug):
    work = Work.objects.get(slug=slug)

    if request.method == 'POST':
        technicians = request.POST.getlist('technicians')
        work.technicians.set(technicians)

    return redirect('work-details',slug=work.slug)

@login_required
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