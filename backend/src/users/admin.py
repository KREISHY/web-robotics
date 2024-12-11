from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from users.models import User, EmailVerify, PasswordReset


@admin.register(User)
class CustomUser(UserAdmin):
    list_display = ('email' , 'username', 'first_name', 'last_name', 'patronymic', 'is_active','email_confirmed',)
    fieldsets = (
        (None, {'fields': ('email', 'username',  'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'patronymic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('last_login', 'date_joined',  'email_confirmed',)

@admin.register(EmailVerify)
class Token(ModelAdmin):
    list_display = ('user','code', 'url', 'created_date',)
    fieldsets = (
        ('Token info', {'fields': ('user', 'url', 'code', 'created_date')}),
    )
    readonly_fields = ('user', 'code', 'url', 'created_date',)


@admin.register(PasswordReset)
class PasswordResetAdmin(ModelAdmin):
    list_display = ('email', 'code', 'url', 'created_date',)
    fieldsets = (
        ('Reset Info', {'fields': ('email', 'code', 'url', 'created_date')}),
    )
    readonly_fields = ('email', 'code', 'url', 'created_date',)
