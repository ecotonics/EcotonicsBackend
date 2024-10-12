from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def technicians(request):
    context = {
        'main' : 'workforce',
        'sub' : 'technicians'
    }
    return render(request,'workforce/technicians.html',context)

@login_required
def add_technician(request):
    context = {
        'main' : 'workforce',
        'sub' : 'technicians'
    }
    return render(request,'workforce/technician-add.html',context)

@login_required
def edit_technician(request):
    context = {
        'main' : 'workforce',
        'sub' : 'technicians'
    }
    return render(request,'workforce/technician-edit.html',context)

@login_required
def technician_details(request):
    context = {
        'main' : 'workforce',
        'sub' : 'technicians'
    }
    return render(request,'workforce/technician-details.html',context)

@login_required
def delete_technician(request):
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