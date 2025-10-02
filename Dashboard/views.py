from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Customers.models import Customer
from Works.models import OnCall
from django.db.models import Count

# Create your views here.

@login_required
def dashboard(request):
    customers = Customer.active_objects.all()
    oncall_qs = OnCall.objects.annotate(num_staffs=Count("staffs"))

    context = {
        'main' : 'dashboard',
        'customers' : customers,
        'pending_works' : oncall_qs.filter(num_staffs=0),
        'ongoing_works' : oncall_qs.filter(num_staffs__gt=0)
    }
    return render(request,'dashboard/index.html',context)