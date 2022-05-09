from django.urls import path
from . import views

urlpatterns = [

    # shared urls
    ################################################################
    path('', views.base),
    path('base/', views.base, name='base'),
    path('register_page/', views.register_page, name='registerPage'),
    path('loginPage/', views.loginPage, name="loginPage"),
    path('logoutUser/', views.logoutUser, name="logoutUser"),
    path('profile_page/', views.profile_page, name="profilePage"),

    # requester urls
    ################################################################
    path('requester_requests/', views.requester_requests, name='r_requests'),
    path('requester_messages/', views.requester_messages, name='r_messages'),
    path('update_request/<str:id>/', views.update_request, name='update_request'),
    path('delete_request/<str:id>/', views.delete_request, name='delete_request'),
    path('requester_my_requests/',views.requester_my_requests,name='r_my_requests'),
    path('requester_amendment/<str:id>/', views.requester_amendment, name='requester_amendment'),

    # maintainer urls
    ################################################################
    path('maintainer_requests/', views.maintainer_requests, name='m_requests'),
    path('maintainer_hard_drives/', views.maintainer_hard_drives, name='m_hard_drives'),
    path('maintainer_return_hard_drives/', views.maintainer_return_hard_drives, name='m_return_hard_drives'),
    path('maintainer_messages/', views.maintainer_messages, name='m_messages'),
    path('maintainer_reports/', views.maintainer_reports, name='m_reports'),
    path('maintainer_configurations/', views.maintainer_configurations, name='m_configurations'),
    path('update_hard_drive/<str:id>/', views.update_hard_drive, name='u_hard_drive'),
    path('delete_hard_drive/<str:id>/', views.delete_hard_drive, name='d_hard_drive'),

    # auditor urls
    ################################################################
    path('auditor_hard_drives/', views.auditor_hard_drives, name='a_hard_drives'),
    path('auditor_messages/', views.auditor_messages, name='a_messages'),
    path('auditor_reports/', views.auditor_reports, name='a_reports'),
    path('auditor_log/', views.auditor_log, name='a_log'),

    # maintainer-configurations urls
    ################################################################
    path('update_configurations_request_status_choice/<str:id>/', views.update_configurations_request_status_choice,
         name='u_configurations_request_status_choice'),
    path('delete_configurations_request_status_choice/<str:id>/', views.delete_configurations_request_status_choice,
         name='d_configurations_request_status_choice'),

    path('update_configurations_requester_status_choice/<str:id>/', views.update_configurations_requester_status_choice,
         name='u_configurations_requester_status_choice'),
    path('delete_configurations_requester_status_choice/<str:id>/', views.delete_configurations_requester_status_choice,
         name='d_configurations_requester_status_choice'),

    path('update_configurations_maintainer_status_choice/<str:id>/',
         views.update_configurations_maintainer_status_choice,
         name='u_configurations_maintainer_status_choice'),
    path('delete_configurations_maintainer_status_choice/<str:id>/',
         views.delete_configurations_maintainer_status_choice,
         name='d_configurations_maintainer_status_choice'),

    path('update_configurations_auditor_status_choice/<str:id>/', views.update_configurations_auditor_status_choice,
         name='u_configurations_auditor_status_choice'),
    path('delete_configurations_auditor_status_choice/<str:id>/', views.delete_configurations_auditor_status_choice,
         name='d_configurations_auditor_status_choice'),

    path('update_configurations_event_status_choice/<str:id>/', views.update_configurations_event_status_choice,
         name='u_configurations_event_status_choice'),
    path('delete_configurations_event_status_choice/<str:id>/', views.delete_configurations_event_status_choice,
         name='d_configurations_event_status_choice'),

    path('update_configurations_event_duration_choice/<str:id>/', views.update_configurations_event_duration_choice,
         name='u_configurations_event_duration_choice'),
    path('delete_configurations_event_duration_choice/<str:id>/', views.delete_configurations_event_duration_choice,
         name='d_configurations_event_duration_choice'),

    path('update_configurations_event_type_choice/<str:id>/', views.update_configurations_event_type_choice,
         name='u_configurations_event_type_choice'),
    path('delete_configurations_event_type_choice/<str:id>/', views.delete_configurations_event_type_choice,
         name='d_configurations_event_type_choice'),

    path('update_configurations_hard_drive_classification_choice/<str:id>/',
         views.update_configurations_hard_drive_classification_choice,
         name='u_configurations_hard_drive_classification_choice'),
    path('delete_configurations_hard_drive_classification_choice/<str:id>/',
         views.delete_configurations_hard_drive_classification_choice,
         name='d_configurations_hard_drive_classification_choice'),

    path('update_configurations_hard_drive_boot_test_status_choice/<str:id>/',
         views.update_configurations_hard_drive_boot_test_status_choice,
         name='u_configurations_hard_drive_boot_test_status_choice'),
    path('delete_configurations_hard_drive_boot_test_status_choice/<str:id>/',
         views.delete_configurations_hard_drive_boot_test_status_choice,
         name='d_configurations_hard_drive_boot_test_status_choice'),

    path('update_configurations_hard_drive_size_choice/<str:id>/',
         views.update_configurations_hard_drive_size_choice,
         name='u_configurations_hard_drive_size_choice'),
    path('delete_configurations_hard_drive_size_choice/<str:id>/',
         views.delete_configurations_hard_drive_size_choice,
         name='d_configurations_hard_drive_size_choice'),

    path('update_configurations_hard_drive_status_choice/<str:id>/',
         views.update_configurations_hard_drive_status_choice,
         name='u_configurations_hard_drive_status_choice'),
    path('delete_configurations_hard_drive_status_choice/<str:id>/',
         views.delete_configurations_hard_drive_status_choice,
         name='d_configurations_hard_drive_status_choice'),
]
