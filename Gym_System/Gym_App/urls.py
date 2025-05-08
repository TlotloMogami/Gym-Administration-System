from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.loginPage),
    path("dashboard/", views.dashboard, name = 'dashboard'),
    path("members/" , views.members, name='members'),
    path("trainers/" , views.trainers, name='trainers'),
    path("payments/" , views.payments, name='payments'),
    path("general_employees/" , views.general_employees, name='general_employees'),
    path("reports/" , views.reports, name='reports'),
    path("register_members/" , views.register_members, name='register_members'),
    path("login/", views.loginPage ,name='loginpage'),
    path("class_scheduling/", views.class_scheduling ,name='class_scheduling')
]