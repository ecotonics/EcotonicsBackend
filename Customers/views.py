from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def intividuals(request):
    context = {
        'main' : 'customers',
        'sub' : 'intivituals'
    }
    return render(request,'customers/intivituals.html',context)

@login_required
def enterprises(request):
    context = {
        'main' : 'customers',
        'sub' : 'enterprises'
    }
    return render(request,'customers/enterprises.html',context)

@login_required
def add_customer(request):
    context = {
        'main' : 'customers',
        'sub' : 'customers'
    }
    return render(request,'customers/customer-add.html',context)

@login_required
def edit_customer(request,cid):
    context = {
        'main' : 'customers',
        'sub' : 'customers'
    }
    return render(request,'customers/customer-edit.html',context)

@login_required
def delete_customer(request,cid):
    return redirect('customers')

#-----------------------------------------------------------------------------------------------------------------------------------

@login_required
def leads(request):
    context = {
        'main' : 'leads',
    }
    return render(request,'leads/leads.html',context)

@login_required
def add_lead(request):
    context = {
        'main' : 'leads',
    }
    return render(request,'leads/lead-add.html',context)

@login_required
def edit_lead(request,cid):
    context = {
        'main' : 'leads',
    }
    return render(request,'leads/lead-edit.html',context)

@login_required
def delete_lead(request,cid):
    return redirect('leads')