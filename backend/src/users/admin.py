from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from users.models import User


@admin.register(User)
class CustomUser(UserAdmin):
    list_display = ('email','first_name', 'last_name', 'patronymic', 'is_active','email_confirmed',)
    fieldsets = (
        (None, {'fields': ('email',  'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'patronymic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'username', 'email_confirmed',)