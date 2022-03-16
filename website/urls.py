from django.urls import path
from . import views

urlpatterns = [
    path('', views.base),
    path('base/', views.base, name='base'),
    path('base_requester/', views.requester, name='requester'),
    path('base_maintainer/', views.maintainer, name='maintainer'),
    path('base_auditor/', views.auditor, name='auditor'),
    path('register/', views.registerPage, name='registerPage'),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('logoutUser/', views.logoutUser, name="logoutUser"),
    path('requests/', views.requests, name='requests'),
    path('hardDrives/', views.hard_drives, name='hardDrives'),
    path('messages/', views.messages, name='messages'),
    path('reports/', views.reports, name='reports'),
    path('configurations/', views.configurations, name='configurations'),
]
