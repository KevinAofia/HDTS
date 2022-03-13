from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, 'pages/main.html')
def requester(request):
    return render(request, 'pages/requester.html')
def maintainer(request):
    return render(request, 'pages/maintainer.html')
def auditor(request):
    return render(request, 'pages/auditor.html')
