from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Customers.models import Customer
from django.contrib import messages

# Create your views here.

@login_required
def customers(request,type):
    customers = Customer.objects.filter(type=type)
    context = {
        'main' : 'customers',
        'sub' : type,
        'type' : type,
        'customers' : customers
    }
    return render(request,'customers/customers.html',context)

@login_required
def add_customer(request,type):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')

        try:
            Customer.objects.create(
                type=type, name=name, location=location, mobile=mobile, email=email
            )
            messages.success(request,'Customer added successfully ... !')
            return redirect('customers',type=type)

        except Exception as exception:
            messages.warning(request,exception)
            return redirect('add-customer',type=type)

    context = {
        'main' : 'customers',
        'sub' : type
    }
    return render(request,'customers/customer-add.html',context)

@login_required
def edit_customer(request,slug):
    customer = Customer.objects.get(slug=slug)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.location = request.POST.get('location')
        customer.mobile = request.POST.get('mobile')
        customer.email = request.POST.get('email')

        try:
            customer.save()
            messages.success(request,'Customer details edited successfully ... !')
            return redirect('customers',type=customer.type)

        except Exception as exception:
            messages.warning(request,exception)
            return redirect('edit-customer',slug=customer.slug)

    context = {
        'main' : 'customers',
        'sub' : customer.type,
        'customer' : customer
    }
    return render(request,'customers/customer-edit.html',context)

@login_required
def delete_customer(request,slug):
    try:
        customer = Customer.objects.get(slug=slug)
        customer.is_deleted=True
        customer.save()
        messages.error(request, 'Customer deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('customers',type=customer.type)

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