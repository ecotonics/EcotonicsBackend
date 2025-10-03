from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from Customers.models import Customer
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count
from Works.models import OnCall, Attendance
from Accounts.models import Transaction

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def customers(request,type):
    customers = Customer.active_objects.filter(type=type).order_by('name')
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
def customer_details(request,slug):
    customer = Customer.objects.get(slug=slug)
    transactions = Transaction.active_objects.filter(on_call__customer=customer)

    revanue_amount = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense_amount = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    net_amount = float(revanue_amount) - float(expense_amount)

    attandances = Attendance.active_objects.filter(on_call__customer=customer)
    attendance_summary = (
        attandances.values("staff__id", "staff__user__first_name", "staff__user__last_name")
        .annotate(total_days=Count("date", distinct=True))
        .order_by("-total_days")
    )

    on_calls = OnCall.active_objects.filter(customer=customer)

    context = {
        'main' : 'customers',
        'sub' : customer.type,
        'customer' : customer,
        'on_calls' : on_calls,
        'attandances' : attandances,
        'attendance_summary' : attendance_summary,
        'transactions' : transactions,
        'revanue_amount' : revanue_amount,
        'expense_amount' : expense_amount,
        'net_amount' : net_amount
    }

    return render(request, 'customers/customer-details.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_customer(request,slug):
    try:
        customer = Customer.objects.get(slug=slug)
        customer.status='inactive'
        customer.save()
        messages.error(request, 'Customer deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

    return redirect('customers',type=customer.type)


def filter_customers(request):
    type = request.GET.get('type')

    customers_list = Customer.active_objects.filter(type=type, status='active').values('slug', 'name')
    customers_data = list(customers_list)

    return JsonResponse({'customers': customers_data})