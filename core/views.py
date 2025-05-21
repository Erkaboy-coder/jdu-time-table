from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Lesson, Notification
from .forms import LessonForm, RegisterForm
from django.contrib.auth import login

def is_admin(user):
    return user.role in ['admin', 'superadmin']


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            if user.role == 'student':
                group = form.cleaned_data['group']
                user.group = group  # Agar `User` modelda group bo‘lsa
                user.save()
            login(request, user)
            return redirect('home')  # kerakli sahifaga o'zgartiring
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def role_based_redirect(request):
    if request.user.role in ['admin', 'superadmin']:
        return redirect('lesson_list')
    elif request.user.role in ['student', 'teacher']:
        return redirect('timetable')
    else:
        return redirect('login')  # nomaʼlum role bo‘lsa
    
@login_required
@user_passes_test(is_admin)
def lesson_list(request):
    lessons = Lesson.objects.all().order_by('start_time')
    return render(request, 'core/lesson_list.html', {'lessons': lessons})

@login_required
@user_passes_test(is_admin)
def lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            message = f"New lesson scheduled: {lesson.subject} on {lesson.start_time.strftime('%Y-%m-%d %H:%M')}"
            notify_users(lesson, message)
            return redirect('lesson_list')
    else:
        form = LessonForm()
    return render(request, 'core/lesson_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            message = f"Lesson updated: {lesson.subject} on {lesson.start_time.strftime('%Y-%m-%d %H:%M')}"
            notify_users(lesson, message)
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'core/lesson_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def lesson_cancel(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.is_canceled = True
    lesson.save()
    message = f"Lesson canceled: {lesson.subject} on {lesson.start_time.strftime('%Y-%m-%d %H:%M')}"
    notify_users(lesson, message)
    return redirect('lesson_list')

def notify_users(lesson, message):
    users = list(lesson.students.all()) + [lesson.teacher]
    for user in users:
        Notification.objects.create(user=user, lesson=lesson, message=message)

@login_required
def notifications_view(request):
    notifications = request.user.notification_set.filter(is_read=False).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')

@login_required
def timetable_view(request):
    if request.user.role == 'student':
        lessons = Lesson.objects.filter(students=request.user, is_canceled=False).order_by('start_time')
    elif request.user.role == 'teacher':
        lessons = Lesson.objects.filter(teacher=request.user, is_canceled=False).order_by('start_time')
    else:
        lessons = Lesson.objects.filter(is_canceled=False).order_by('start_time')
    return render(request, 'core/timetable.html', {'lessons': lessons})
