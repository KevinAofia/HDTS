from django.urls import path
from . import views

urlpatterns = [

    # shared urls
    ################################################################
    path('', views.base),
    path('base/', views.base, name='base'),
    path('registerPage/', views.registerPage, name='registerPage'),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('logoutUser/', views.logoutUser, name="logoutUser"),

    # requester urls
    ################################################################
    path('base_requester/', views.requester, name='requester'),
    path('requester_requests/', views.requester_requests, name='r_requests'),
    path('requester_messages/', views.requester_messages, name='r_messages'),

    # maintainer urls
    ################################################################
    path('base_maintainer/', views.maintainer, name='maintainer'),
    path('maintainer_requests/', views.maintainer_requests, name='m_requests'),
    path('maintainer_hard_drives/', views.maintainer_hard_drives, name='m_hard_drives'),
    path('maintainer_messages/', views.maintainer_messages, name='m_messages'),
    path('maintainer_reports/', views.maintainer_reports, name='m_reports'),
    path('maintainer_configurations/', views.maintainer_configurations, name='m_configurations'),

    # auditor urls
    ################################################################
    path('base_auditor/', views.auditor, name='auditor'),
    path('auditor_hard_drives/', views.auditor_hard_drives, name='a_hard_drives'),
    path('auditor_messages/', views.auditor_messages, name='a_messages'),
    path('auditor_reports/', views.auditor_reports, name='a_reports'),

]
