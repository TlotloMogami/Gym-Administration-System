from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import delete_class

urlpatterns = [ 
    path("", views.loginPage),
    path("dashboard/", views.dashboard, name = 'dashboard'),
    path("members/" , views.members, name='members'),
    path("trainers/" , views.trainers, name='trainers'),
    path("payments/" , views.payments, name='payments'),
    path("reports/" , views.reports, name='reports'),
    path("reports_api/reports/" , views.reports_api, name='reports_api'),
    path("login/", views.loginPage ,name='loginpage'),
    path("class_scheduling/", views.class_scheduling ,name='class_scheduling'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('members-add/', views.add_member, name='add_member'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('trainers/add/', views.add_trainer, name='add_trainer'),
    path('trainers/edit/<int:id>/', views.edit_trainer, name='edit_trainer'),
    path('trainers/delete/<int:id>/', views.delete_trainer, name='delete_trainer'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('api/schedule-class/', views.schedule_class, name='schedule_class'),
    path('api/trainers/', views.get_trainers_by_category, name='get_trainers_by_category'),
    path('api/delete-class/<int:class_id>/', views.delete_class, name='delete_class')

]
