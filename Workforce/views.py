from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Users.models import User
from Workforce.models import Department, Designation, Staff
from django.contrib import messages
from django.db import transaction
from Works.models import Attendance, OnCall
from django.db.models import Count, Sum
from datetime import datetime
from Accounts.models import Transaction, TransactionCategory, Wage
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
        # 'designations,' : designations,
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
    staff = Staff.active_objects.get(slug=slug)
    on_calls = OnCall.active_objects.filter(staffs__in=[staff])
    wages = Wage.active_objects.filter(staff=staff).order_by('-updated')
    attandances = Attendance.active_objects.filter(staff=staff)
    categories = TransactionCategory.active_objects.filter(type='EXPENSE')
    payments = Transaction.active_objects.filter(staff=staff)

    wage_total = attandances.aggregate(total=Sum('wage'))['total'] or 0.00
    wage_paid = payments.aggregate(total=Sum('amount'))['total'] or 0.00
    wage_balance = float(wage_total) - float(wage_paid)

    context = {
        'main' : 'workforce',
        'sub' : 'staffs',
        'staff' : staff,
        'wages' : wages,
        'attandances' : attandances,
        'wage_total' : wage_total,
        'wage_paid' : wage_paid,
        'wage_balance' : wage_balance,
        'on_calls' : on_calls,
        'today' : today,
        'categories' : categories,
        'payments' : payments
    }

    return render(request,'workforce/staff-details.html',context)

@login_required
def delete_staff(request,slug):
    try:
        staff = Staff.objects.get(slug=slug)
        staff.status = 'inactive'
        staff.save()
        messages.error(request, 'staff status changed successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)
    return redirect('staffs')

@login_required
def add_attandance(request, slug):
    on_call = OnCall.active_objects.filter(slug=slug).first()

    if request.method == 'POST':
        technician = request.POST.get('technician')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        try:
            staff = Staff.objects.get(slug=technician)
            wage_object = Wage.active_objects.filter(staff=staff).order_by('-updated').first()
            
            if wage_object:
                wage = wage_object.amount
            else:
                wage = staff.staff_wage

            Attendance.objects.create(
                staff=staff, on_call=on_call, date=date, start_time=start_time, end_time=end_time, wage=wage
            )

            messages.success(request,'Attendance added successfully')
            return redirect('on-call-details', slug=slug)

        except Exception as exception:
            messages.warning(request,exception)
            return redirect('on-call-details', slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def delete_attandance(request, slug):
    try:
        attendance = Attendance.active_objects.filter(slug=slug).first()
        attendance.is_deleted = True
        attendance.save()

        messages.success(request, 'Attendance deleted')
    except Exception as exception:
        messages.warning(request, str(exception))

    return redirect('on-call-details', slug=attendance.on_call.slug)


@user_passes_test(lambda u: u.is_superuser)
def update_wage(request, slug):
    staff = Staff.objects.get(slug=slug)

    if request.method == 'POST':
        updated = request.POST.get('updated')
        amount = request.POST.get('amount')

        try:
            Wage.objects.create(staff=staff, updated=updated, amount=amount)
            messages.success(request,'Wage updated successfully ... !')

        except Exception as exception:
            messages.warning(request,str(exception))

    return redirect('staff-details', slug=staff.slug)


@user_passes_test(lambda u: u.is_superuser)
def delete_wage(request, slug):
    try:
        wage = Wage.objects.get(slug=slug)
        wage.is_deleted=True
        wage.save()
        messages.success(request, 'Wage deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('staff-details', slug=wage.staff.slug)

@user_passes_test(lambda u: u.is_superuser)
def add_payment(request, slug):
    staff = Staff.objects.get(slug=slug)

    if request.method == 'POST':
        date = request.POST.get('date')
        category_slug = request.POST.get('category')
        site_slug = request.POST.get('on_call')
        amount = request.POST.get('amount')
        title = request.POST.get('title')

        try:
            category = TransactionCategory.active_objects.get(slug=category_slug)
            on_call = OnCall.active_objects.get(slug=site_slug)

            Transaction.objects.create(
                date=date, type='EXPENSE', category=category, staff=staff,
                title=title, amount=amount, on_call=on_call
            )

            messages.success(request,'Payment added successfully ... !')

        except Exception as exception:
            messages.warning(request,str(exception))

    return redirect('staff-details', slug=staff.slug)

@user_passes_test(lambda u: u.is_superuser)
def delete_payment(request, slug):
    try:
        transaction = Transaction.objects.get(slug=slug)
        transaction.is_deleted=True
        transaction.save()
        messages.success(request, 'Payment deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('staff-details', slug=transaction.staff.slug)