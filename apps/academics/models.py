from django.db import models

# Create your models here.



class Programme(models.Model):
    programme_id = models.CharField(max_length=20, unique=True)
    programme_name = models.CharField(max_length=100)
    programme_code = models.CharField(max_length=20, unique=True)
    duration = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.programme_name


class Level(models.Model):
    level_name = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return self.level_name


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ("FIRST", "First Semester"),
        ("SECOND", "Second Semester"),
    ]

    semester_name = models.CharField(
        max_length=20,
        choices=SEMESTER_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_semester_name_display()


class AcademicSession(models.Model):
    session_name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.session_name
