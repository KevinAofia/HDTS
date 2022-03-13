from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'pages/home.html')


def requester(request):
    return render(request, 'pages/base_requester.html')


def maintainer(request):
    return render(request, 'pages/base_maintainer.html')


def auditor(request):
    return render(request, 'pages/base_auditor.html')


def requests(request):
    return render(request, 'pages/requests.html')


def hardDrives(request):
    return render(request, 'pages/hardDrives.html')


def messages(request):
    return render(request, 'pages/messages.html')


def reports(request):
    return render(request, 'pages/reports.html')


def configurations(request):
    return render(request, 'pages/configurations.html')
