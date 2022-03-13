from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.main),
    path('requester/', views.requester),
    path('maintainer/', views.maintainer),
    path('auditor/', views.auditor),
]
