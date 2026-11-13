
from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'matric_number',
        'user',
        'programme',
        'level',
        'admission_year',
    )

    search_fields = (
        'matric_number',
        'user__email',
        'user__first_name',
        'user__last_name',
    )

    list_filter = (
        'programme',
        'level',
        'admission_year',
    )

    list_select_related = (
        'user',
        'programme',
        'level',
    )
