
from django.contrib import admin
from .models import Programme, Level, Semester, AcademicSession


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        'programme_id',
        'programme_name',
        'programme_code',
        'duration',
    )

    search_fields = (
        'programme_id',
        'programme_name',
        'programme_code',
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):

    list_display = ('level_name',)
    search_fields = ('level_name',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):

    list_display = ('semester_name',)


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):

    list_display = (
        'session_name',
        'start_date',
        'end_date',
        'is_current',
    )

    list_filter = ('is_current',)
    search_fields = ('session_name',)
