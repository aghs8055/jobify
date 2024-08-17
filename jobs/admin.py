from django.contrib import admin

from jobs.models import Job, Category, Application


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class OwnerOrSuperuserAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.employer == request.user.employer
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.employer == request.user.employer
        return super().has_delete_permission(request, obj)


@admin.register(Job)
class JobAdmin(OwnerOrSuperuserAdmin):
    fields = [
        "title",
        "description",
        "category",
        "salary",
        "time_type",
        "seniority",
        "contract_type",
        "location",
        "expire_at",
        "is_active",
    ]
    list_display = [
        "title",
        "category",
        "salary",
        "time_type",
        "seniority",
        "contract_type",
        "location",
        "expire_at",
        "is_active",
    ]
    search_fields = ["title", "description"]
    list_filter = ["category", "time_type", "seniority", "contract_type", "location", "is_active"]
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        obj.employer = request.user.employer
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(employer=request.user.employer)


@admin.register(Application)
class ApplicationAdmin(OwnerOrSuperuserAdmin):
    fields = ["resume", "status", "description"]
    list_display = ["applicant", "job", "status"]
    search_fields = ["job__title", "applicant__email", "applicant__first_name", "applicant__last_name"]
    list_filter = ["status"]
    ordering = ["updated_at"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(job__employer=request.user.employer)
