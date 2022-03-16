from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateBasicUserForm, CreateRequester, LoginForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required

def base(request):
    return render(request, 'pages/base.html')


@unauthenticated_user
def registerPage(request):
    register_form = CreateBasicUserForm()
    if request.method == 'POST':
        register_form = CreateBasicUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()

            group = Group.objects.get(name='requester')
            user.groups.add(group)

            return redirect('loginPage')  # redirect to login following registration

    context = {
        'register_form': register_form
    }
    return render(request, 'pages/register.html', context)

@unauthenticated_user
def loginPage(request):
    login_form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')
    context = {
        'login_form': login_form
    }
    return render(request, 'pages/loginPage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin','requester'])
def requester(request):
    return render(request, 'pages/base_requester.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin','maintainer'])
def maintainer(request):
    return render(request, 'pages/base_maintainer.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin','auditor'])
def auditor(request):
    return render(request, 'pages/base_auditor.html')

@login_required(login_url='loginPage')
def requests(request):
    return render(request, 'pages/requests.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin','maintainer'])
def hard_drives(request):
    hard_drives_object = HardDrive.objects.all()
    context = {
        'hard_drives': hard_drives_object
    }
    return render(request, 'pages/hardDrives.html', context)

@login_required(login_url='loginPage')
def messages(request):
    return render(request, 'pages/messages.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin','auditor'])
def reports(request):
    return render(request, 'pages/reports.html')

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin','maintainer'])
def configurations(request):
    return render(request, 'pages/configurations.html')
