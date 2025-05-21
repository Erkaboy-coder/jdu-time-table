from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Room, Lesson, Notification, Group  # Group model ham qo‘shildi

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'group', 'is_staff', 'is_active']
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'group')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'group')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group)  # Group modelini ham ro‘yxatdan o‘tkazamiz
admin.site.register(Room)
admin.site.register(Lesson)
admin.site.register(Notification)
