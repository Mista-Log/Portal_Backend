
from django.contrib import admin
from .models import College, Department, Programme, Session


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")
    search_fields = ("name", "code")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "college")
    list_filter = ("college",)
    search_fields = ("name", "code")


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "department")
    list_filter = ("department",)
    search_fields = ("name", "code")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_active",
        "is_registration_open",
    )
    list_filter = ("is_active", "is_registration_open")
    search_fields = ("name",)
