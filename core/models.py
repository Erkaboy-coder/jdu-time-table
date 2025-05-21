from django.contrib.auth.models import AbstractUser
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User,
        limit_choices_to={'role': 'teacher'},
        on_delete=models.CASCADE,
        related_name='lessons_as_teacher'  # Bu yerda related_name qo'shildi
    )
    students = models.ManyToManyField(
        User,
        limit_choices_to={'role': 'student'},
        blank=True,
        related_name='lessons_as_student'  # Bu yerda ham related_name qo'shildi
    )
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    groups = models.ManyToManyField(Group, related_name='lessons')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} by {self.teacher.username} in {self.room.name} at {self.start_time}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
