from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL
    path('schedules/', views.class_schedule_list, name='class-schedule-list'),
    path('schedules/new/', views.create_class_schedule, name='create-class-schedule'),
    path('classes/', views.class_list, name='class-list'),
    path('attendance/<int:class_id>/', views.take_attendance, name='take-attendance'),
]

