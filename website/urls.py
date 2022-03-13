from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('base_requester/', views.requester),
    path('base_maintainer/', views.maintainer),
    path('base_auditor/', views.auditor),
    path('requests/', views.requests),
    path('hardDrives/', views.hardDrives),
    path('messages/', views.messages),
    path('reports/', views.reports),
    path('configurations/', views.configurations),
]
