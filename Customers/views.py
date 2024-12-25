from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Customers.models import Customer
from django.contrib import messages
from Services.models import Category, Service
from Customers.models import Lead, Followup
from django.apps import apps
from django.http import JsonResponse
from Technicians.models import Technician
from Works.models import Requisition
from django.db.models import Count
from Works.models import Work

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def customers(request,type):
    customers = Customer.active_objects.filter(type=type)
    context = {
        'main' : 'customers',
        'sub' : type,
        'type' : type,
        'customers' : customers
    }
    return render(request,'customers/customers.html',context)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def delete_customer(request,slug):
    try:
        customer = Customer.objects.get(slug=slug)
        customer.is_deleted=True
        customer.save()
        messages.error(request, 'Customer deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('customers',type=customer.type)


def filter_customers(request):
    type = request.GET.get('type')

    customers_list = Customer.active_objects.filter(type=type).values('slug', 'name')
    customers_data = list(customers_list)

    return JsonResponse({'customers': customers_data})


@user_passes_test(lambda u: u.is_superuser)
def leads(request,status):
    leads = Lead.active_objects.filter(status=status.upper())
    context = {
        'main' : 'leads',
        'sub' : status,
        'status' : status,
        'leads' : leads
    }
    return render(request,'leads/leads.html',context)

@user_passes_test(lambda u: u.is_superuser)
def add_lead(request):
    categories = Category.active_objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        category = request.POST.get('category')
        service = request.POST.get('service')
        info = request.POST.get('info')
        lead_type = request.POST.get('lead_type')
        work_type = request.POST.get('work_type')
        customer = request.POST.get('customer')

        try:
            category = Category.objects.get(slug=category)
            service = Service.objects.get(slug=service)

            if lead_type == 'new':
                Lead.objects.create(
                    type=work_type, category=category, service=service, info=info,
                    name=name, email=email, mobile=mobile, location=location,
                )

            elif lead_type == 'existing':
                customer = Customer.objects.get(slug=customer)
                Lead.objects.create(
                    type=work_type, category=category, service=service, info=info, customer=customer,
                    name=customer.name, email=customer.email, mobile=customer.mobile, location=customer.location,
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
    staffs = Technician.active_objects.all()

    context = {
        'main' : 'leads',
        'sub' : lead.status.lower(),
        'lead' : lead,
        'followups' : followups,
        'staffs' : staffs,
    }
    return render(request,'leads/lead-details.html',context)

@user_passes_test(lambda u: u.is_superuser)
def convert_lead(request,slug):
    try:
        lead = Lead.objects.get(slug=slug)
        lead.status = 'CONVERTED'
        work = Work.objects.create(lead=lead)
        work.technicians.set(lead.staffs.all())
        lead.save()
        return redirect('works',status='pending')
    
    except Exception as exception:
        messages.warning(request,exception)
        return redirect('lead-view',slug=lead.slug)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def edit_lead(request,slug):
    lead = Lead.objects.get(slug=slug)
    categories = Category.active_objects.all()
    services = Service.active_objects.filter(category=lead.category)
    customers = Customer.active_objects.all()

    if request.method == 'POST':
        if lead.customer:
            customer = request.POST.get('customer')
            customer = Customer.objects.get(slug=customer)
            lead.customer = customer

            lead.name = customer.name
            lead.email = customer.email
            lead.mobile = customer.mobile
            lead.location = customer.location
        else:
            lead.name = request.POST.get('name')
            lead.mobile = request.POST.get('mobile')
            lead.email = request.POST.get('email')
            lead.location = request.POST.get('location')

        lead.type = request.POST.get('type')
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
            return redirect('lead-edit', slug=slug)

    context = {
        'main' : 'leads',
        'sub' : lead.status.lower(),
        'lead' : lead,
        'categories' : categories,
        'services' : services,
        'customers' : customers
    }
    return render(request,'leads/lead-edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def delete_lead(request,slug):
    try:
        lead = Lead.objects.get(slug=slug)
        lead.status = 'FAILED'
        lead.save()
        messages.error(request, 'Marked the lead as failed ...!')

    except Exception as exception:
        messages.warning(request, exception)
    return redirect('leads',status=lead.status)

@user_passes_test(lambda u: u.is_superuser)
def assign_staff(request, slug):
    lead = Lead.active_objects.get(slug=slug)
    staffs = request.POST.getlist('staffs')
    lead.staffs.set(staffs)
    lead.save()
    return redirect('lead-view',slug=lead.slug)

@login_required
def update_requirements(request, slug):
    lead = Lead.objects.get(slug=slug)

    if request.method == 'POST':
        lead.primary_requirements = request.POST.get('primary_requirements')
        lead.scope_of_work = request.POST.get('scope_of_work')
        lead.site_condetion = request.POST.get('site_condetion')
        lead.additional_requirements = request.POST.get('additional_requirements')
        lead.customer_preferences = request.POST.get('customer_preferences')

        try:
            lead.save()
            messages.success(request, 'Requirements updated successfully')
            return redirect('lead-view', slug=lead.slug)
        
        except Exception as exception:
            messages.warning(request, str(exception))
            return redirect('update-requirements', slug=lead.slug)

    context = {
        'main' : 'leads',
        'sub' : lead.status.lower(),
        'lead' : lead,
    }
    return render(request, 'leads/requirements.html', context)

@user_passes_test(lambda u: u.is_superuser)
def lead_update_toggle(request, slug):
    lead = Lead.objects.get(slug=slug)
    lead.is_update_allowed = not lead.is_update_allowed
    lead.save()
    return redirect('lead-view', slug=lead.slug)