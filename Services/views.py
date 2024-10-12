from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Services.models import Category
from django.contrib import messages

# Create your views here.

@login_required
def categories(request):
    categories = Category.active_objects.all()

    context = {
        'main' : 'services',
        'sub' : 'categories',
        'categories' : categories
    }
    return render(request,'services/categories.html',context)

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        info = request.POST.get('info')

        try:
            Category.objects.create(name=name,info=info)
            messages.success(request,'Category added successfully ... !')
            return redirect('categories')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('category-add')

    context = {
        'main' : 'services',
        'sub' : 'categories'
    }
    return render(request,'services/category-add.html',context)

@login_required
def edit_category(request,slug):
    category = Category.objects.get(slug=slug)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.info = request.POST.get('info')

        try:
            category.save()
            messages.success(request,'Category edited successfully ... !')
            return redirect('categories')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('category-edit' , slug=category.slug)

    context = {
        'main' : 'services',
        'sub' : 'categories',
        'category' : category
    }
    return render(request,'services/category-edit.html',context)

@login_required
def delete_category(request,slug):
    try:
        category = Category.objects.get(slug=slug)
        category.is_deleted=True
        category.save()
        messages.error(request, 'Category deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)

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