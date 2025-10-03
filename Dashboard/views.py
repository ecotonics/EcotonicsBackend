from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Customers.models import Customer
from Works.models import OnCall, Task
from django.db.models import Count

from datetime import datetime
today = datetime.today()

# Create your views here.

@login_required
def dashboard(request):
    customers = Customer.active_objects.all()
    oncall_qs = OnCall.active_objects.all()
    tasks_qs = Task.active_objects.all()

    context = {
        'main' : 'dashboard',
        'customers' : customers,
        'pending_works' : oncall_qs.filter(status='pending'),
        'ongoing_works' : oncall_qs.filter(status='ongoing'),
        'completed_works' : oncall_qs.filter(status='completed'),
        'today_tasks' : tasks_qs.filter(date=today),
        'overdue_tasks' : tasks_qs.filter(date__lt=today),
        'upcoming_tasks' : tasks_qs.filter(date__gt=today),
    }
    return render(request,'dashboard/index.html',context)