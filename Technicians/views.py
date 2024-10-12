from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Users.models import User
from Technicians.models import Department, Designation, Technician
from django.contrib import messages
from django.db import transaction

# Create your views here.

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

    context = {
        'main' : 'workforce',
        'sub' : 'technicians',
        'technician' : technician
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

#-----------------------------------------------------------------------------------------------------------------------------------

@login_required
def attandance(request):
    context = {
        'main' : 'workforce',
        'sub' : 'attandance'
    }
    return render(request,'workforce/attandance.html',context)

@login_required
def add_attandance(request):
    context = {
        'main' : 'workforce',
        'sub' : 'attandance'
    }
    return render(request,'workforce/attandance-add.html',context)

@login_required
def edit_attandance(request):
    context = {
        'main' : 'workforce',
        'sub' : 'attandance'
    }
    return render(request,'workforce/attandance-edit.html',context)

@login_required
def delete_attandance(request):
    return redirect('attandance')