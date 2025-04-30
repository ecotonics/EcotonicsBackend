from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from Services.models import Category, Service
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from Works.models import Work

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories = Category.active_objects.all().annotate(services=Count('service')).order_by('name')

    context = {
        'main' : 'services',
        'sub' : 'categories',
        'categories' : categories
    }

    return render(request,'services/categories.html',context)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def category_details(request,slug):
    category = Category.objects.get(slug=slug)
    services = Service.active_objects.filter(category=category)

    context = {
        'main' : 'services',
        'sub' : 'categories',
        'category' : category,
        'services' : services
    }
    return render(request,'services/category-details.html',context)

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def services(request):
    services = Service.active_objects.all().order_by('category')

    context = {
        'main' : 'services',
        'sub' : 'services',
        'services' : services
    }

    return render(request,'services/services.html',context)

@user_passes_test(lambda u: u.is_superuser)
def add_service(request):
    categories = Category.active_objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        info = request.POST.get('info')

        try:
            category = Category.objects.get(auto_id=category_id)
            Service.objects.create(name=name,category=category,info=info)
            messages.success(request,'Service added successfully ...!')
            return redirect('services')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('service-add')

    context = {
        'main' : 'services',
        'sub' : 'services',
        'categories' : categories
    }

    return render(request,'services/service-add.html',context)

@user_passes_test(lambda u: u.is_superuser)
def edit_service(request,slug):
    categories = Category.active_objects.all()
    service = Service.objects.get(slug=slug)

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.info = request.POST.get('info')
        category_id = request.POST.get('category')

        try:
            category = Category.objects.get(auto_id=category_id)
            service.category = category
            service.save()
            messages.success(request,'Service edited successfully ...!')
            return redirect('services')

        except Exception as exception:
            messages.warning(request,str(exception))
            return redirect('service-edit',slug=service.slug)

    context = {
        'main' : 'services',
        'sub' : 'services',
        'service' : service,
        'categories' : categories
    }

    return render(request,'services/service-edit.html',context)

@user_passes_test(lambda u: u.is_superuser)
def delete_service(request,slug):
    try:
        service = Service.objects.get(slug=slug)
        service.is_deleted=True
        service.save()
        messages.error(request, 'Service deleted successfully ...!')

    except Exception as exception:
        messages.warning(request, exception)
    return redirect('services')

@user_passes_test(lambda u: u.is_superuser)
def service_details(request,slug):
    service = Service.active_objects.get(slug=slug)
    works = Work.objects.filter(lead__service=service)

    context = {
        'main' : 'services',
        'sub' : 'services',
        'service' : service,
        'works' : works,
    }

    return render(request,'services/service-details.html',context)

#-----------------------------------------------------------------------------------------------------------------------------------

def filter_service(request):
    slug = request.GET.get('slug')
    services_list = Service.active_objects.filter(category__slug=slug).values('slug', 'name')
    services_data = list(services_list)

    return JsonResponse({'services': services_data})