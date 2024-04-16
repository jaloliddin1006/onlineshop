from django.contrib import admin
from .models import User, UserResetPasswordCode
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'username')


@admin.register(UserResetPasswordCode)
class UserResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ('private_id', 'email', 'code', 'expiration_time', 'is_confirmation')
    list_display_links = ('private_id', 'email')
