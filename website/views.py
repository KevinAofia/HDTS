from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import CreateUserForm, LoginForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required


def base(request):
    return render(request, 'pages/base.html')


@unauthenticated_user
def registerPage(request):
    register_form = CreateUserForm()
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()

            group = Group.objects.get(name='requester')
            user.groups.add(group)
            Requester.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )
            Maintainer.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )
            Auditor.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
            )

            return redirect('loginPage')  # redirect to login following registration

    context = {
        'register_form': register_form
    }
    return render(request, 'pages/registerPage.html', context)


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
    return redirect('base')


# requester views
################################################################
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester(request):
    if request.user.groups.filter(name='admin').exists():
        my_requests = Request.objects.all()
    else:
        my_requests = request.user.requester.request_set.all()
    context = {
        'my_requests': my_requests
    }
    return render(request, 'pages/base_requester.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester_requests(request):
    return render(request, 'pages/requester_requests.html', {})


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester_messages(request):
    return render(request, 'pages/requester_messages.html')


# maintainer views
################################################################
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer(request):
    requesters = Requester.objects.all()
    maintainers = Maintainer.objects.all()
    auditors = Auditor.objects.all()
    requests = Request.objects.all()
    events = Event.objects.all()
    hard_drives = HardDrive.objects.all()
    requester_group = Group.objects.get(name="requester").user_set.all()
    maintainer_group = Group.objects.get(name="maintainer").user_set.all()
    auditor_group = Group.objects.get(name="auditor").user_set.all()

    context = {
        'requesters': requesters,
        'maintainers': maintainers,
        'auditors': auditors,
        'requests': requests,
        'events': events,
        'hard_drives': hard_drives,
        'requester_group': requester_group,
        'maintainer_group': maintainer_group,
        'auditor_group': auditor_group,
    }
    return render(request, 'pages/base_maintainer.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_requests(request):
    return render(request, 'pages/maintainer_requests.html', {})


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_hard_drives(request):
    hard_drives_object = HardDrive.objects.all()
    context = {
        'hard_drives': hard_drives_object
    }
    return render(request, 'pages/maintainer_hard_drives.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_messages(request):
    return render(request, 'pages/maintainer_messages.html')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_reports(request):
    return render(request, 'pages/maintainer_reports.html')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_configurations(request):
    return render(request, 'pages/maintainer_configurations.html')


# auditor views
################################################################
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'auditor'])
def auditor(request):
    return render(request, 'pages/base_auditor.html')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'auditor'])
def auditor_hard_drives(request):
    hard_drives_object = HardDrive.objects.all()
    context = {
        'hard_drives': hard_drives_object
    }
    return render(request, 'pages/auditor_hard_drives.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'auditor'])
def auditor_messages(request):
    return render(request, 'pages/auditor_messages.html')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'auditor'])
def auditor_reports(request):
    return render(request, 'pages/auditor_reports.html')
