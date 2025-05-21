from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_based_redirect, name='home'), 
    path('register/', views.register_view, name='register'),
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:pk>/cancel/', views.lesson_cancel, name='lesson_cancel'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('timetable/', views.timetable_view, name='timetable'),
]
