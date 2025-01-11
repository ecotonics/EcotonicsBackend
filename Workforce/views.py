from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Users.models import User
from Workforce.models import Department, Designation, Staff
from django.contrib import messages
from django.db import transaction
from Works.models import Work, Attendance
from django.db.models import Count, Sum
from Customers.models import Lead
from datetime import datetime
from Accounts.models import Transaction
today = datetime.today()

# Create your views here.

@login_required
def departments(request):
    departments = Department.active_objects.all().annotate(staffs=Count('staff')).order_by('name')

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
    staffs = Staff.active_objects.filter(department=department)

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
    designations = Designation.active_objects.all().annotate(staffs=Count('staff')).order_by('department')

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
    staffs = Staff.active_objects.filter(designation=designation)

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
def staffs(request):
    staffs = Staff.active_objects.all().order_by('user__first_name')

    context = {
        'main' : 'workforce',
        'sub' : 'staffs',
        'staffs' : staffs
    }

    return render(request,'workforce/staffs.html',context)

@login_required
def add_staff(request):
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
                user = User.objects.create(username=username,first_name=name,email=email,is_staff=True,photo=photo,mobile=mobile)
                user.set_password(password)
                user.save()

                Staff.objects.create(
                    user=user,location=location,aadhar=aadhar,blood=blood,
                    department=department,designation=designation,contact_name=contact_name,contact_number=contact_number,
                    relation=relation,address=address
                )
                messages.success(request,'staff added successfully ...!')
                return redirect('staffs')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('staff-add')

    context = {
        'main' : 'workforce',
        'sub' : 'staffs',
        'departments' : departments,
        'designations' : designations
    }

    return render(request,'workforce/staff-add.html',context)

@login_required
def edit_staff(request,slug):
    departments = Department.active_objects.all()
    designations = Designation.active_objects.all()
    staff = Staff.objects.get(slug=slug)

    if request.method == 'POST':
        if len(request.FILES) > 0:
            staff.user.photo = request.FILES.get('photo')

        staff.user.first_name = request.POST.get('name')
        staff.user.mobile = request.POST.get('mobile')
        staff.user.email = request.POST.get('email')
        staff.location = request.POST.get('location')
        staff.aadhar = request.POST.get('aadhar')
        staff.blood = request.POST.get('bg')

        staff.contact_name = request.POST.get('contact_name')
        staff.contact_number = request.POST.get('contact_number')
        staff.relation = request.POST.get('relation')
        staff.address = request.POST.get('address')

        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')

        try:
            with transaction.atomic():
                department = Department.objects.get(auto_id=department_id)
                designation = Designation.objects.get(auto_id=designation_id)
                staff.department = department
                staff.designation = designation
                staff.user.save()
                staff.save()

                messages.success(request,'staff details edited successfully ...!')
                return redirect('staffs')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('staff-edit',slug=slug)

    context = {
        'main' : 'workforce',
        'sub' : 'staffs',
        'departments' : departments,
        'designations' : designations,
        'staff' : staff
    }

    return render(request,'workforce/staff-edit.html',context)

@login_required
def staff_details(request,slug):
    staff = Staff.objects.get(slug=slug)
    sites = Lead.active_objects.filter(staffs__in=[staff], status='PENDING')
    works = Work.active_objects.filter(staffs__in=[staff])
    attendances = Attendance.objects.filter(staff=staff)
    expenses = Transaction.active_objects.filter(staff=staff).order_by('-id')
    self_expense = expenses.filter(source='SELF').aggregate(total=Sum('amount'))['total']
    petty_expense = expenses.filter(source='PETTY').aggregate(total=Sum('amount'))['total']
    credit_expense = expenses.filter(source='CREDIT').aggregate(total=Sum('amount'))['total']
    petty_balance = 0.0

    context = {
        'main' : 'workforce',
        'sub' : 'staffs',
        'staff' : staff,
        'sites' : sites,
        'works' : works,
        'attendances' : attendances,
        'expenses' : expenses,
        'self_expense' : self_expense,
        'petty_expense' : petty_expense,
        'credit_expense' : credit_expense,
        'petty_balance' : petty_balance
    }

    return render(request,'workforce/staff-details.html',context)

@login_required
def delete_staff(request,slug):
    try:
        staff = Staff.objects.get(slug=slug)
        staff.status = 0
        staff.save()
        messages.error(request, 'staff status changed successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)
    return redirect('staffs')


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
    staffs = Staff.active_objects.all()
    works = Work.active_objects.all()

    if request.method == 'POST':
        staff = request.POST.get('staff')
        work = request.POST.get('work')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        try:
            if request.user.is_superuser:
                staff = Staff.objects.get(slug=staff)
            else:
                staff = Staff.objects.get(user=request.user)

            work = Work.objects.get(slug=work)

            Attendance.objects.create(
                staff=staff, work=work, start_time=start_time, end_time=end_time
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
        'staffs' : staffs,
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