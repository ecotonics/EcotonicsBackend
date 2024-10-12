from django.shortcuts import render,redirect
from Users.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#------------------------------------------------- SIGN IN ---------------------------------------------------#

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'incorrect username or password')
            return redirect('.')
    return render(request,'users/sign-in.html')

#----------------------------------------------CHANGE PASSWORD -----------------------------------------------#

@login_required
def changepassword(request):
    user = request.user
    if request.method == 'POST':
        currentPassword = request.POST.get('currentPassword')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')

        if not user.check_password(currentPassword):
            messages.error(request, 'Incorrect current password')
            return redirect('change-password')
        elif newPassword != confirmPassword:
            messages.error(request,'Password and confirm password does not match try again')
            return redirect('change-password')
        else:
            user.set_password(confirmPassword)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password changed login again')
            return redirect('dashboard')

    return render(request,'Auth/change-password.html')

#------------------------------------------------- SIGN OUT --------------------------------------------------#

@login_required
def signout(request):
    logout(request)
    return redirect('sign-in')