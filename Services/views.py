from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def categories(request):
    context = {
        'main' : 'services',
        'sub' : 'categories'
    }
    return render(request,'services/categories.html',context)

@login_required
def add_category(request):
    context = {
        'main' : 'services',
        'sub' : 'categories'
    }
    return render(request,'services/category-add.html',context)

@login_required
def edit_category(request,cid):
    context = {
        'main' : 'services',
        'sub' : 'categories'
    }
    return render(request,'services/category-edit.html',context)

@login_required
def delete_category(request,cid):
    return redirect('categories')

#-----------------------------------------------------------------------------------------------------------------------------------

@login_required
def services(request):
    context = {
        'main' : 'services',
        'sub' : 'services'
    }
    return render(request,'services/services.html',context)

@login_required
def add_service(request):
    context = {
        'main' : 'services',
        'sub' : 'services'
    }
    return render(request,'services/service-add.html',context)

@login_required
def edit_service(request,cid):
    context = {
        'main' : 'services',
        'sub' : 'services'
    }
    return render(request,'services/service-edit.html',context)

@login_required
def delete_service(request,cid):
    return redirect('services')

#-----------------------------------------------------------------------------------------------------------------------------------

@login_required
def calls(request):
    context = {
        'main' : 'calls'
    }
    return render(request,'calls/calls.html',context)

@login_required
def add_call(request):
    context = {
        'main' : 'calls'
    }
    return render(request,'calls/call-add.html',context)