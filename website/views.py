from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import AmendmentForm, RegisterForm, RegisterFormAddOns, LoginForm, CreateRequestForm, CreateEventForm, ReturnHardDriveForm, UpdateProfileForm, \
    UpdateRequestForm, UpdateEventForm, CreateOrUpdateRequestStatusChoiceForm, CreateOrUpdateRequesterStatusChoiceForm, \
    CreateOrUpdateMaintainerStatusChoiceForm, CreateOrUpdateAuditorStatusChoiceForm, \
    CreateOrUpdateEventStatusChoiceForm, CreateOrUpdateEventDurationChoiceForm, CreateOrUpdateEventTypeChoiceForm, \
    CreateOrUpdateHardDriveClassificationChoiceForm, CreateOrUpdateHardDriveBootTestStatusChoiceForm, \
    CreateOrUpdateHardDriveSizeChoiceForm, CreateOrUpdateHardDriveStatusChoiceForm, UpdateRequestFormAll, \
    UpdateEventFormAll, CreateOrUpdateHardDriveForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from datetime import date, datetime


def base(request):
    return render(request, 'pages/base.html')


@unauthenticated_user
def register_page(request):
    register_form = RegisterForm()
    register_form_add_ons = RegisterFormAddOns()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        register_form_add_ons = RegisterFormAddOns(request.POST)
        if register_form.is_valid() and register_form_add_ons.is_valid():
            user = register_form.save()
            user_add_ons = register_form_add_ons.save(commit=False)
            group = Group.objects.get(name='requester')
            user.groups.add(group)
            UserProfile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                direct_supervisor_email=user_add_ons.direct_supervisor_email,
                branch_chief_email=user_add_ons.branch_chief_email,
                requester_status=RequesterStatusChoice.objects.first(),
                maintainer_status=MaintainerStatusChoice.objects.first(),
                auditor_status=AuditorStatusChoice.objects.first(),
            )
            messages.success(request, 'Account was created for ' + user.username)
            return redirect('loginPage')  # redirect to login following registration
        else:
            messages.error(request, 'Registration was unsuccessful')

    context = {
        'register_form': register_form,
        'register_form_add_ons': register_form_add_ons
    }
    return render(request, 'pages/register_page.html', context)


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
        else:
            messages.error(request, 'Login was unsuccessful')

    context = {
        'login_form': login_form
    }
    return render(request, 'pages/loginPage.html', context)


def logoutUser(request):
    logout(request)
    return redirect('base')


# profile views
################################################################
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester', 'maintainer', 'auditor'])
def profile_page(request):
    user = UserProfile.objects.get(user=request.user)
    update_profile_form = UpdateProfileForm(instance=user)
    if request.method == 'POST':
        update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=user)

        if update_profile_form.is_valid():
            update_profile_form.save()
            messages.success(request, 'Account was successfully updated')
        else:
            messages.error(request, 'Account was unsuccessful updating')

        return redirect('profilePage')

    profiles = UserProfile.objects.all()

    context = {
        'update_profile_form': update_profile_form,
        'profiles': profiles,
    }
    return render(request, 'pages/profile_page.html', context)


# requester views
################################################################
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester_requests(request):
    event_form = CreateEventForm()
    request_form = CreateRequestForm()
    if request.method == 'POST':
        event_form = CreateEventForm(request.POST)
        request_form = CreateRequestForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event was successfully created.')
        if request_form.is_valid():
            request_info = request_form.save(commit=False)  # wait to save request until all fields are specified
            date_time_object = datetime.now()
            Request.objects.create(
                user=request.user,
                event=request_info.event,
                requester=request_info.requester,
                # request_number format: MMDDYYYY/requesterfirstinitial_requesterlastinitial/devcomHHMMSS
                request_number=str(date_time_object.year) + str(date_time_object.month) + str(
                    date_time_object.day) + str(request.user.first_name[0]) + str(
                    request.user.last_name[0]) + "devcom" + str(date_time_object.hour) + str(
                    date_time_object.minute) + str(date_time_object.second),
                pickup_date=request_info.pickup_date,
                number_of_classified_hard_drives_needed=request_info.number_of_classified_hard_drives_needed,
                number_of_unclassified_hard_drives_needed=request_info.number_of_unclassified_hard_drives_needed,
                status=RequestStatusChoice.objects.first(),
                comment=request_info.comment,
            )
            Log.objects.create(
                user=request.user,
                timestamp = date_time_object.today(),
                action_performed = 'Create a Request'
            )
            messages.success(request, 'Request was successfully created.')
        return redirect('r_requests')
    requests = Request.objects.all()  # passing all requests
    request_status_choice = RequestStatusChoice.objects.all()  # pass first option
    context = {
        'request_form': request_form,
        'event_form': event_form,
        'requests': requests,
        'request_status_choice': request_status_choice
    }
    return render(request, 'pages/requester_requests.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester', 'maintainer'])
def update_request(request, id):
    this_request = Request.objects.get(id=id)
    update_request_form = UpdateRequestForm(instance=this_request)
    update_event_form = UpdateEventForm(instance=this_request.event)
    update_request_form_all = UpdateRequestFormAll(instance=this_request)
    update_event_form_all = UpdateEventFormAll(instance=this_request.event)

    if request.method == 'POST':
        update_request_form = UpdateRequestForm(request.POST, instance=this_request)
        update_event_form = UpdateEventForm(request.POST, instance=this_request.event)

        update_request_form_all = UpdateRequestFormAll(request.POST, instance=this_request)
        update_event_form_all = UpdateEventFormAll(request.POST, instance=this_request.event)
        date_time_object = datetime.now()

        if update_request_form.is_valid() and update_event_form.is_valid() and "ALL" not in request.POST:
            update_request_form.save()
            update_event_form.save()
            Log.objects.create(
                user=request.user,
                timestamp = date_time_object.today(),
                action_performed = 'Update a Request'
            )
            messages.success(request, 'Request was successfully updated.')
            return redirect('r_requests')

        elif update_request_form_all.is_valid() and update_event_form_all.is_valid() and "ALL" in request.POST:
            update_request_form_all.save()
            update_event_form_all.save()
            Log.objects.create(
                user=request.user,
                timestamp = date_time_object.today(),
                action_performed = 'Update a Request'
            )
            messages.success(request, 'Request was successfully updated.')
            return redirect('m_requests')
        else:
            messages.error(request, 'Request update was unsuccessful.')
            return redirect('r_requests')

    if request.user.groups.filter(name="maintainer").exists() or request.user.groups.filter(name="admin").exists():
        can_edit = True
    else:
        can_edit = False

    context = {
        'this_request': this_request,
        'update_request_form': update_request_form,
        'update_event_form': update_event_form,
        'can_edit': can_edit,
        'update_request_form_all': update_request_form_all,
        'update_event_form_all': update_event_form_all,
    }
    return render(request, 'pages/update_request.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester', 'maintainer'])
def delete_request(request, id):
    this_request = Request.objects.get(id=id)
    if request.method == 'POST':
        this_request.delete()
        messages.success(request, 'Request was successfully deleted.')
        return redirect('r_requests')
    if request.user.groups.filter(name="maintainer").exists() or request.user.groups.filter(name="admin").exists():
        can_edit = True
    else:
        can_edit = False
    context = {
        'this_request': this_request,
        'can_edit':can_edit,
    }
    return render(request, 'pages/delete_request.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester_my_requests(request):
    this_user = UserProfile.objects.get(user=request.user)
    # print(this_user)
    my_requests = Request.objects.all()  # passing all requests
    # print(my_requests.status)
    context = {
        'requests': my_requests,
        'user':this_user
    }
    return render(request, 'pages/requester_my_requests.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester_messages(request):
    return render(request, 'pages/requester_messages.html')


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'requester'])
def requester_amendment(request,id):
    submitted = False

    # this_user = UserProfile.objects.get(user=request.user)
    my_request = Request.objects.get(id=id)
    # date_time_object = datetime.now().today
    today = str(datetime.today().date())
    form = AmendmentForm()

    if request.method == "POST":
        form = AmendmentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)  # wait to save request until all fields are specified
            date_time_object = datetime.now()
            Amendment.objects.create(
                user=request.user,
                amendment_decison_date = form.amendment_decison_date,
                amendment_submission_date = today,
                amendment_description = form.amendment_description,
                comment = form.comment
            )


    context = {
        'amendment_form': form,
        'requests':my_request
    }
    return render(request, 'pages/requester_amendment.html', context)



# maintainer views
################################################################
# view all requests (allow updating, deletion, adding a request)
# view all hard drives
# assign hard drives to a request, maybe this includes filtering through HDs

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_requests(request):
    requests = Request.objects.all()  # passing all requests
    request_status_choice = RequestStatusChoice.objects.all()
    context = {
        'requests': requests,
        'request_status_choice':request_status_choice,
    }
    return render(request, 'pages/maintainer_requests.html', context)



@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_return_hard_drives(request):
    choice = HardDriveStatusChoice.objects.all
    return_drive_form = ReturnHardDriveForm()

    if request.method == 'POST':
        return_drive_form = ReturnHardDriveForm(request.POST)
        if return_drive_form.is_valid():
            return_drive_form = return_drive_form.save(commit=False)  
            this_drive = HardDrive.objects.get(serial_number=return_drive_form.serial_number)
            this_drive.status = choice.available
            return_drive_form.save()
            messages.success(request, 'Hard drive was successfully returned.')
            return redirect('m_hard_drives')
        else:
            messages.error(request, 'Hard drive could not be returned..')
            return redirect('m_hard_drives')

    context = {
        'return_drive_form': return_drive_form
    }
    return render(request, 'pages/maintainer_return_hard_drives.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def maintainer_hard_drives(request):
    hard_drives = HardDrive.objects.all()
    hard_drive_form = CreateOrUpdateHardDriveForm()

    if request.method == 'POST':
        hard_drive_form = CreateOrUpdateHardDriveForm(request.POST)
        if hard_drive_form.is_valid():
            hard_drive_form.save()
            messages.success(request, 'Hard drive was successfully added to inventory.')
            return redirect('m_hard_drives')
        else:
            messages.error(request, 'Hard drive could not be added to inventory.')
            return redirect('m_hard_drives')

    context = {
        'hard_drives': hard_drives,
        'hard_drive_form': hard_drive_form
    }
    return render(request, 'pages/maintainer_hard_drives.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_hard_drive(request, id):
    this_hard_drive = HardDrive.objects.get(id=id)
    update_hard_drive_form = CreateOrUpdateHardDriveForm(instance=this_hard_drive)

    if request.method == 'POST':
        update_hard_drive_form = CreateOrUpdateHardDriveForm(request.POST, instance=this_hard_drive)

        if update_hard_drive_form.is_valid():
            update_hard_drive_form.save()
            messages.success(request, 'Hard drive was successfully updated.')
            return redirect('m_hard_drives')
        else:
            messages.error(request, 'Hard drive update was unsuccessful.')
            return redirect('m_hard_drives')

    context = {
        'this_hard_drive': this_hard_drive,
        'update_hard_drive_form': update_hard_drive_form,
    }
    return render(request, 'pages/update_hard_drive.html', context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_hard_drive(request, id):
    this_hard_drive = HardDrive.objects.get(id=id)
    if request.method == 'POST':
        this_hard_drive.delete()
        messages.success(request, 'Hard drive was successfully deleted.')
        return redirect('m_hard_drives')
    context = {
        'this_hard_drive': this_hard_drive,
    }
    return render(request, 'pages/delete_hard_drive.html', context)


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
    request_status_choice = RequestStatusChoice.objects.all()
    requester_status_choice = RequesterStatusChoice.objects.all()
    maintainer_status_choice = MaintainerStatusChoice.objects.all()
    auditor_status_choice = AuditorStatusChoice.objects.all()
    event_status_choice = EventStatusChoice.objects.all()
    event_duration_choice = EventDurationChoice.objects.all()
    event_type_choice = EventTypeChoice.objects.all()
    hard_drive_classification_choice = HardDriveClassificationChoice.objects.all()
    hard_drive_boot_test_status_choice = HardDriveBootTestStatusChoice.objects.all()
    hard_drive_size_choice = HardDriveSizeChoice.objects.all()
    hard_drive_status_choice = HardDriveStatusChoice.objects.all()

    request_status_choice_form = CreateOrUpdateRequestStatusChoiceForm()
    requester_status_choice_form = CreateOrUpdateRequesterStatusChoiceForm()
    maintainer_status_choice_form = CreateOrUpdateMaintainerStatusChoiceForm()
    auditor_status_choice_form = CreateOrUpdateAuditorStatusChoiceForm()
    event_status_choice_form = CreateOrUpdateEventStatusChoiceForm()
    event_duration_choice_form = CreateOrUpdateEventDurationChoiceForm()
    event_type_choice_form = CreateOrUpdateEventTypeChoiceForm()
    hard_drive_classification_choice_form = CreateOrUpdateHardDriveClassificationChoiceForm()
    hard_drive_boot_test_status_choice_form = CreateOrUpdateHardDriveBootTestStatusChoiceForm()
    hard_drive_size_choice_form = CreateOrUpdateHardDriveSizeChoiceForm()
    hard_drive_status_choice_form = CreateOrUpdateHardDriveSizeChoiceForm()

    if request.method == 'POST':
        request_status_choice_form = CreateOrUpdateRequestStatusChoiceForm(request.POST)
        requester_status_choice_form = CreateOrUpdateRequesterStatusChoiceForm(request.POST)
        maintainer_status_choice_form = CreateOrUpdateMaintainerStatusChoiceForm(request.POST)
        auditor_status_choice_form = CreateOrUpdateAuditorStatusChoiceForm(request.POST)
        event_status_choice_form = CreateOrUpdateEventStatusChoiceForm(request.POST)
        event_duration_choice_form = CreateOrUpdateEventDurationChoiceForm(request.POST)
        event_type_choice_form = CreateOrUpdateEventTypeChoiceForm(request.POST)
        hard_drive_classification_choice_form = CreateOrUpdateHardDriveClassificationChoiceForm(request.POST)
        hard_drive_boot_test_status_choice_form = CreateOrUpdateHardDriveBootTestStatusChoiceForm(request.POST)
        hard_drive_size_choice_form = CreateOrUpdateHardDriveSizeChoiceForm(request.POST)
        hard_drive_status_choice_form = CreateOrUpdateHardDriveStatusChoiceForm(request.POST)
        if request_status_choice_form.is_valid() and "config1" in request.POST:
            request_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if requester_status_choice_form.is_valid() and "config2" in request.POST:
            requester_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if maintainer_status_choice_form.is_valid() and "config3" in request.POST:
            maintainer_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if auditor_status_choice_form.is_valid() and "config4" in request.POST:
            auditor_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if event_status_choice_form.is_valid() and "config5" in request.POST:
            event_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if event_duration_choice_form.is_valid() and "config6" in request.POST:
            event_duration_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if event_type_choice_form.is_valid() and "config7" in request.POST:
            event_type_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if hard_drive_classification_choice_form.is_valid() and "config8" in request.POST:
            hard_drive_classification_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if hard_drive_boot_test_status_choice_form.is_valid() and "config9" in request.POST:
            hard_drive_boot_test_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if hard_drive_size_choice_form.is_valid() and "config10" in request.POST:
            hard_drive_size_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')
        if hard_drive_status_choice_form.is_valid() and "config11" in request.POST:
            hard_drive_status_choice_form.save()
            messages.success(request, 'Configuration successfully created.')
            return redirect('m_configurations')

    context = {
        'request_status_choice': request_status_choice,
        'requester_status_choice': requester_status_choice,
        'maintainer_status_choice': maintainer_status_choice,
        'auditor_status_choice': auditor_status_choice,
        'event_status_choice': event_status_choice,
        'event_duration_choice': event_duration_choice,
        'event_type_choice': event_type_choice,
        'hard_drive_classification_choice': hard_drive_classification_choice,
        'hard_drive_boot_test_status_choice': hard_drive_boot_test_status_choice,
        'hard_drive_size_choice': hard_drive_size_choice,
        'hard_drive_status_choice': hard_drive_status_choice,
        'request_status_choice_form': request_status_choice_form,
        'requester_status_choice_form': requester_status_choice_form,
        'maintainer_status_choice_form': maintainer_status_choice_form,
        'auditor_status_choice_form': auditor_status_choice_form,
        'event_status_choice_form': event_status_choice_form,
        'event_duration_choice_form': event_duration_choice_form,
        'event_type_choice_form': event_type_choice_form,
        'hard_drive_classification_choice_form': hard_drive_classification_choice_form,
        'hard_drive_boot_test_status_choice_form': hard_drive_boot_test_status_choice_form,
        'hard_drive_size_choice_form': hard_drive_size_choice_form,
        'hard_drive_status_choice_form':hard_drive_status_choice_form

    }
    return render(request, 'pages/maintainer_configurations.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_request_status_choice(request, id):
    this_configuration = RequestStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateRequestStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateRequestStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_request_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_request_status_choice(request, id):
    this_configuration = RequestStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_request_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_requester_status_choice(request, id):
    this_configuration = RequesterStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateRequesterStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateRequesterStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_requester_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_requester_status_choice(request, id):
    this_configuration = RequesterStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_requester_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_maintainer_status_choice(request, id):
    this_configuration = MaintainerStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateMaintainerStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateMaintainerStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_maintainer_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_maintainer_status_choice(request, id):
    this_configuration = MaintainerStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_maintainer_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_auditor_status_choice(request, id):
    this_configuration = AuditorStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateAuditorStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateAuditorStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_auditor_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_auditor_status_choice(request, id):
    this_configuration = AuditorStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_auditor_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_event_status_choice(request, id):
    this_configuration = EventStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateEventStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateEventStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_event_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_event_status_choice(request, id):
    this_configuration = EventStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_event_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_event_duration_choice(request, id):
    this_configuration = EventDurationChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateEventDurationChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateEventDurationChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_event_duration_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_event_duration_choice(request, id):
    this_configuration = EventDurationChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_event_duration_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_event_type_choice(request, id):
    this_configuration = EventTypeChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateEventTypeChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateEventTypeChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_event_type_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_event_type_choice(request, id):
    this_configuration = EventTypeChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_event_type_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_hard_drive_classification_choice(request, id):
    this_configuration = HardDriveClassificationChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateHardDriveClassificationChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateHardDriveClassificationChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_hard_drive_classification_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_hard_drive_classification_choice(request, id):
    this_configuration = EventTypeChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_hard_drive_classification_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_hard_drive_boot_test_status_choice(request, id):
    this_configuration = HardDriveBootTestStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateHardDriveBootTestStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateHardDriveBootTestStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_hard_drive_boot_test_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_hard_drive_boot_test_status_choice(request, id):
    this_configuration = HardDriveBootTestStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_hard_drive_boot_test_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_hard_drive_size_choice(request, id):
    this_configuration = HardDriveSizeChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateHardDriveSizeChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateHardDriveSizeChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_hard_drive_size_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_hard_drive_size_choice(request, id):
    this_configuration = HardDriveSizeChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_hard_drive_size_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def update_configurations_hard_drive_status_choice(request, id):
    this_configuration = HardDriveStatusChoice.objects.get(id=id)
    update_configuration_form = CreateOrUpdateHardDriveStatusChoiceForm(instance=this_configuration)
    if request.method == 'POST':
        update_configuration_form = CreateOrUpdateHardDriveStatusChoiceForm(request.POST, instance=this_configuration)
        if update_configuration_form.is_valid():
            update_configuration_form.save()
            messages.success(request, 'Configuration was successfully updated.')
            return redirect('m_configurations')
        else:
            messages.error(request, 'Configuration was unsuccessful updating.')
            return redirect('m_configurations')
    context = {
        'this_configuration': this_configuration,
        'update_configuration_form': update_configuration_form
    }
    return render(request, 'pages/update_configurations_hard_drive_status_choice.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'maintainer'])
def delete_configurations_hard_drive_status_choice(request, id):
    this_configuration = HardDriveStatusChoice.objects.get(id=id)
    if request.method == 'POST':
        this_configuration.delete()
        messages.success(request, 'Configuration was successfully deleted.')
        return redirect('m_configurations')
    context = {'this_configuration': this_configuration}
    return render(request, 'pages/delete_configurations_hard_drive_status_choice.html', context)



# auditor views
################################################################
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


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin', 'auditor'])
def auditor_log(request):

    logs = Log.objects.all()  # passing all logs
    context = {
        'log': logs,
    }

    return render(request, 'pages/auditor_log.html', context)

    