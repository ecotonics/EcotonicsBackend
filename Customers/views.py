from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Customers.models import Customer
from django.contrib import messages
from Services.models import Category, Service
from Customers.models import Lead, Followup
from django.apps import apps

# Create your views here.

@login_required
def customers(request,type):
    customers = Customer.active_objects.filter(type=type)
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


@login_required
def leads(request,status):
    leads = Lead.active_objects.filter(status=status.upper())
    context = {
        'main' : 'leads',
        'sub' : status,
        'status' : status,
        'leads' : leads
    }
    return render(request,'leads/leads.html',context)

@login_required
def add_lead(request):
    categories = Category.active_objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        type = request.POST.get('type')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        category = request.POST.get('category')
        service = request.POST.get('service')
        info = request.POST.get('info')

        try:
            category = Category.objects.get(slug=category)
            service = Service.objects.get(slug=service)

            Lead.objects.create(
                name=name,location=location,type=type,mobile=mobile,email=email,category=category,service=service,info=info
            )
            messages.success(request,'Lead addedd successfully')
            return redirect('leads',status='pending')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('lead-add')

    context = {
        'main' : 'leads',
        'sub' : 'pending',
        'categories' : categories
    }
    return render(request,'leads/lead-add.html',context)

@login_required
def view_lead(request,slug):
    lead = Lead.objects.get(slug=slug)
    followups = Followup.active_objects.filter(lead=lead)
    context = {
        'main' : 'leads',
        'sub' : lead.status.lower(),
        'lead' : lead,
        'followups' : followups
    }
    return render(request,'leads/lead-details.html',context)

@login_required
def convert_lead(request,slug):
    lead = Lead.objects.get(slug=slug)
    lead.status = 'CONVERTED'
    lead.save()

    Work = apps.get_model('Works', 'Work')
    Work.objects.create(lead=lead)
    return redirect('works',slug='pending')

@login_required
def followup(request,slug):
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')

        try:
            lead = Lead.objects.get(slug=slug)
            Followup.objects.create(lead=lead,title=title,details=details)
            messages.success(request, 'Followup added successfully')
        except Exception as exception:
            messages.warning(request,exception)

        return redirect('lead-view',slug=lead.slug)

@login_required
def edit_lead(request,slug):
    lead = Lead.objects.get(slug=slug)
    categories = Category.active_objects.all()
    services = Service.active_objects.filter(category=lead.category)

    if request.method == 'POST':
        lead.name = request.POST.get('name')
        lead.location = request.POST.get('location')
        lead.type = request.POST.get('type')
        lead.mobile = request.POST.get('mobile')
        lead.email = request.POST.get('email')
        lead.info = request.POST.get('info')

        category = request.POST.get('category')
        service = request.POST.get('service')

        try:
            category = Category.objects.get(slug=category)
            service = Service.objects.get(slug=service)

            lead.category = category
            lead.service = service
            lead.save()

            messages.success(request,'Lead detailed updated successfully')
            return redirect('leads', status=lead.status.lower())

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('lead-edit',slug=slug)

    context = {
        'main' : 'leads',
        'sub' : lead.status.lower(),
        'lead' : lead,
        'categories' : categories,
        'services' : services
    }
    return render(request,'leads/lead-edit.html',context)

@login_required
def delete_lead(request,slug):
    try:
        lead = Lead.objects.get(slug=slug)
        lead.status = 'FAILED'
        lead.save()
        messages.error(request, 'Marked the lead as failed ...!')

    except Exception as exception:
        messages.warning(request, exception)
    return redirect('leads',status=lead.status)