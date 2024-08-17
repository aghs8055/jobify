from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Employer


class EmployerInline(admin.StackedInline):
    model = Employer
    can_delete = False
    verbose_name_plural = "Employer"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (EmployerInline,)
