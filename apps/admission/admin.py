from django.contrib import admin

from .models import Application, Qualification


class QualificationInline(admin.TabularInline):
    model = Qualification
    extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "application_number",
        "owner",
        "session",
        "eligibility",
        "decision",
    )
    list_filter = ("session", "eligibility", "decision")
    search_fields = ("application_number", "owner__email")
    readonly_fields = ("application_number",)
    inlines = [QualificationInline]