from django import forms
from .models import Lesson, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'groups', 'students', 'room', 'start_time', 'end_time', 'is_canceled']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'students': forms.CheckboxSelectMultiple(),
            'groups': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dastlab students maydonini bo‘sh qilib qo‘yamiz
        self.fields['students'].queryset = User.objects.none()
        
        if 'groups' in self.data:
            try:
                group_ids = self.data.getlist('groups')
                # Guruhdagi studentlarni filterlaymiz
                # Faraz qilamiz, User va Group o‘rtasida ManyToMany maydon nomi 'groups'
                self.fields['students'].queryset = User.objects.filter(
                    groups__id__in=group_ids,
                    role='student'
                ).distinct()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Edit holatida: instance.groups ga qarab studentlarni ko‘rsatish
            self.fields['students'].queryset = self.instance.groups.students.filter(role='student')


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'group', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        group = cleaned_data.get('group')

        if role == 'student' and not group:
            self.add_error('group', "Talaba uchun guruhni tanlash majburiy.")
        return cleaned_data
