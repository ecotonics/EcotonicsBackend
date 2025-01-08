from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Customers.models import Customer, Lead
from Works.models import Work

# Create your views here.

@login_required
def dashboard(request):
    works = Work.active_objects.all()
    customers = Customer.active_objects.all()

    context = {
        'main' : 'dashboard',
        'customers' : customers,
        'pending_works' : works.filter(status='PENDING'),
        'ongoing_works' : works.filter(status='ONGOING'),
        'completed_works' : works.filter(status='COMPLETED')
    }
    return render(request,'dashboard/index.html',context)