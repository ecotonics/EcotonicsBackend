from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Works.models import Work

# Create your views here.

@login_required
def works(request,status):
    works = Work.active_objects.filter(status=status.upper())
    context = {
        'main' : 'works',
        'sub' : status,
        'works' : works,
        'status' : status
    }
    return render(request,'works/works.html',context)

@login_required
def work_details(request,slug):
    work = Work.objects.get(slug=slug)
    context = {
        'main' : 'works',
        'sub' : work.status.lower,
        'work' : work,
    }
    return render(request,'works/work-details.html',context)