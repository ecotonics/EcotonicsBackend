from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Users.models import User
from Technicians.models import Department, Designation, Technician
from django.contrib import messages
from django.db import transaction
from Works.models import Work, Attendance
from django.db.models import Count, Sum
from Customers.models import Lead
from Accounts.models import Expense
from datetime import datetime
today = datetime.today()

# Create your views here.

@login_required
def departments(request):
    departments = Department.active_objects.all().annotate(staffs=Count('technician'))

    context = {
        'main' : 'workforce',
        'sub' : 'departments',
        'departments' : departments
    }

    return render(request, 'workforce/departments.html', context)

@login_required
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        info = request.POST.get('info')

        try:
            Department.objects.create(name=name,info=info)
            messages.success(request,'Department added successfully ... !')
            return redirect('departments')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('department-add')

    context = {
        'main' : 'workforce',
        'sub' : 'departments'
    }

    return render(request,'workforce/department-add.html',context)

@login_required
def edit_department(request,slug):
    department = Department.objects.get(slug=slug)

    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.info = request.POST.get('info')

        try:
            department.save()
            messages.success(request,'Department edited successfully ... !')
            return redirect('departments')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('department-edit' , slug=department.slug)

    context = {
        'main' : 'workforce',
        'sub' : 'departments',
        'department' : department
    }

    return render(request,'workforce/department-edit.html',context)

@login_required
def department_details(request,slug):
    department = Department.objects.get(slug=slug)
    designations = Designation.active_objects.filter(department=department)
    staffs = Technician.active_objects.filter(department=department)

    context = {
        'main' : 'workforce',
        'sub' : 'departments',
        'department' : department,
        'designations,' : designations,
        'staffs' : staffs
    }
    return render(request,'workforce/department-details.html',context)

@login_required
def delete_department(request,slug):
    try:
        department = Department.objects.get(slug=slug)
        department.is_deleted=True
        department.save()
        messages.error(request, 'Department deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('departments')

@login_required
def designations(request):
    designations = Designation.active_objects.all().annotate(staffs=Count('technician'))

    context = {
        'main' : 'workforce',
        'sub' : 'designations',
        'designations' : designations
    }

    return render(request, 'workforce/designations.html', context)

@login_required
def add_designation(request):
    departments = Department.active_objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        info = request.POST.get('info')
        department = request.POST.get('department')

        try:
            department = Department.objects.get(slug=department)

            Designation.objects.create(name=name, info=info, department=department)
            messages.success(request,'Designation added successfully ... !')
            return redirect('designations')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('designation-add')

    context = {
        'main' : 'workforce',
        'sub' : 'designations',
        'departments' : departments
    }

    return render(request,'workforce/designation-add.html',context)

@login_required
def edit_designation(request,slug):
    designation = Designation.objects.get(slug=slug)
    departments = Department.active_objects.all()

    if request.method == 'POST':
        designation.name = request.POST.get('name')
        designation.info = request.POST.get('info')

        department = request.POST.get('department')
        designation.department = Department.objects.get(slug=department)

        try:
            designation.save()
            messages.success(request,'Designation edited successfully ... !')
            return redirect('designations')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('designation-edit' , slug=designation.slug)

    context = {
        'main' : 'workforce',
        'sub' : 'designations',
        'designation' : designation,
        'departments' : departments
    }

    return render(request,'workforce/designation-edit.html',context)

@login_required
def designation_details(request,slug):
    designation = Designation.objects.get(slug=slug)
    staffs = Technician.active_objects.filter(designation=designation)

    context = {
        'main' : 'workforce',
        'sub' : 'designations',
        'designation' : designation,
        'staffs' : staffs
    }
    return render(request,'workforce/designation-details.html',context)

@login_required
def delete_designation(request,slug):
    try:
        designation = Designation.objects.get(slug=slug)
        designation.is_deleted=True
        designation.save()
        messages.error(request, 'Designation deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('designations')

@login_required
def technicians(request):
    technicians = Technician.active_objects.all()

    context = {
        'main' : 'workforce',
        'sub' : 'technicians',
        'technicians' : technicians
    }

    return render(request,'workforce/technicians.html',context)

@login_required
def add_technician(request):
    departments = Department.active_objects.all()
    designations = Designation.active_objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        location = request.POST.get('location')
        aadhar = request.POST.get('aadhar')
        blood = request.POST.get('bg')
        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')

        contact_name = request.POST.get('contact_name')
        contact_number = request.POST.get('contact_number')
        relation = request.POST.get('relation')
        address = request.POST.get('address')

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            with transaction.atomic():
                department = Department.objects.get(auto_id=department_id)
                designation = Designation.objects.get(auto_id=designation_id)
                user = User.objects.create(username=username,first_name=name,email=email,is_technician=True,photo=photo,mobile=mobile)
                user.set_password(password)
                user.save()

                Technician.objects.create(
                    user=user,location=location,aadhar=aadhar,blood=blood,
                    department=department,designation=designation,contact_name=contact_name,contact_number=contact_number,
                    relation=relation,address=address
                )
                messages.success(request,'Technician added successfully ...!')
                return redirect('technicians')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('technician-add')

    context = {
        'main' : 'workforce',
        'sub' : 'technicians',
        'departments' : departments,
        'designations' : designations
    }

    return render(request,'workforce/technician-add.html',context)

@login_required
def edit_technician(request,slug):
    departments = Department.active_objects.all()
    designations = Designation.active_objects.all()
    technician = Technician.objects.get(slug=slug)

    if request.method == 'POST':
        if len(request.FILES) > 0:
            technician.user.photo = request.FILES.get('photo')

        technician.user.first_name = request.POST.get('name')
        technician.user.mobile = request.POST.get('mobile')
        technician.user.email = request.POST.get('email')
        technician.location = request.POST.get('location')
        technician.aadhar = request.POST.get('aadhar')
        technician.blood = request.POST.get('bg')

        technician.contact_name = request.POST.get('contact_name')
        technician.contact_number = request.POST.get('contact_number')
        technician.relation = request.POST.get('relation')
        technician.address = request.POST.get('address')

        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')

        try:
            with transaction.atomic():
                department = Department.objects.get(auto_id=department_id)
                designation = Designation.objects.get(auto_id=designation_id)
                technician.department = department
                technician.designation = designation
                technician.user.save()
                technician.save()

                messages.success(request,'Technician details edited successfully ...!')
                return redirect('technicians')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('technician-edit',slug=slug)

    context = {
        'main' : 'workforce',
        'sub' : 'technicians',
        'departments' : departments,
        'designations' : designations,
        'technician' : technician
    }

    return render(request,'workforce/technician-edit.html',context)

@login_required
def technician_details(request,slug):
    technician = Technician.objects.get(slug=slug)
    sites = Lead.active_objects.filter(staffs__in=[technician], status='PENDING')
    works = Work.active_objects.filter(technicians__in=[technician])
    attendances = Attendance.objects.filter(technician=technician)
    expenses = Expense.active_objects.filter(technician=technician).order_by('-id')
    self_expense = expenses.filter(source='SELF').aggregate(total=Sum('amount'))['total']
    petty_expense = expenses.filter(source='PETTY').aggregate(total=Sum('amount'))['total']
    credit_expense = expenses.filter(source='CREDIT').aggregate(total=Sum('amount'))['total']
    petty_balance = 0.0

    context = {
        'main' : 'workforce',
        'sub' : 'technicians',
        'technician' : technician,
        'sites' : sites,
        'works' : works,
        'attendances' : attendances,
        'expenses' : expenses,
        'self_expense' : self_expense,
        'petty_expense' : petty_expense,
        'credit_expense' : credit_expense,
        'petty_balance' : petty_balance
    }

    return render(request,'workforce/technician-details.html',context)

@login_required
def delete_technician(request,slug):
    try:
        technician = Technician.objects.get(slug=slug)
        technician.status = 0
        technician.save()
        messages.error(request, 'Technician status changed successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)
    return redirect('technicians')


@login_required
def attandance(request):
    attandances = Attendance.active_objects.filter(status='PENDING')
    if request.user.is_superuser:
        clocked = False
    else:
        attandance = Attendance.active_objects.filter(date=today).exists()
        if attandance:
            clocked = True

    context = {
        'main' : 'workforce',
        'sub' : 'attandance',
        'attandances' : attandances,
        'clocked' : clocked
    }
    return render(request,'workforce/attandance.html',context)

@login_required
def add_attandance(request):
    technicians = Technician.active_objects.all()
    works = Work.active_objects.all()

    if request.method == 'POST':
        technician = request.POST.get('technician')
        work = request.POST.get('work')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        try:
            if request.user.is_superuser:
                technician = Technician.objects.get(slug=technician)
            else:
                technician = Technician.objects.get(user=request.user)

            work = Work.objects.get(slug=work)

            Attendance.objects.create(
                technician=technician, work=work, start_time=start_time, end_time=end_time
            )

            messages.success(request,'Attendance added successfully')

            if request.user.is_superuser:
                return redirect('attandance')
            else:
                return redirect('dashboard')

        except Exception as exception:
            messages.warning(request,exception)
            return redirect('attandance-add')

    context = {
        'main' : 'workforce',
        'sub' : 'attandance',
        'technicians' : technicians,
        'works' : works
    }
    return render(request,'workforce/attandance-add.html',context)

@login_required
def edit_attandance(request, slug):
    context = {
        'main' : 'workforce',
        'sub' : 'attandance'
    }
    return render(request,'workforce/attandance-edit.html',context)

@login_required
def delete_attandance(request):
    return redirect('attandance')

@login_required
def approve_attendance(request,slug):
    try:
        attandance = Attendance.objects.get(slug=slug)
        attandance.status = 2
        attandance.save()
        messages.success(request,'Attendance approved')
    except Exception as exception:
        messages.error(request,exception)

    return redirect('attandance')

@login_required
def reject_attendance(request,slug):
    try:
        attandance = Attendance.objects.get(slug=slug)
        attandance.status = 0
        attandance.save()
        messages.success(request,'Attendance rejected')
    except Exception as exception:
        messages.error(request,exception)

    return redirect('attandance')