
from django.contrib import admin
from .models import Course, CourseOffering


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'course_id',
        'course_code',
        'course_title',
        'credit_unit',
    )

    search_fields = (
        'course_id',
        'course_code',
        'course_title',
    )

    list_filter = ('credit_unit',)


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):

    list_display = (
        'course',
        'programme',
        'level',
        'semester',
    )

    list_filter = (
        'programme',
        'level',
        'semester',
    )

    list_select_related = (
        'course',
        'programme',
        'level',
        'semester',
    )

