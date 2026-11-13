
from django.contrib import admin
from .models import SessionRegistration, CourseRegistration


@admin.register(SessionRegistration)
class SessionRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'academic_session',
        'semester',
        'registration_date',
        'registration_status',
    )

    list_filter = (
        'academic_session',
        'semester',
        'registration_status',
    )

    search_fields = (
        'student__matric_number',
    )


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'registration',
        'course_offering',
        'registration_date',
        'registration_status',
    )

    list_filter = (
        'registration_status',
        'registration_date',
    )

    list_select_related = (
        'registration',
        'course_offering',
    )
