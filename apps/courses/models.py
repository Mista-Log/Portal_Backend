
from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True)
    course_code = models.CharField(max_length=20, unique=True)
    course_title = models.CharField(max_length=150)
    credit_unit = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.course_code


class CourseOffering(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='offerings'
    )

    academic_session = models.ForeignKey(
        'academics.AcademicSession',
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    programme = models.ForeignKey(
        'academics.Programme',
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    level = models.ForeignKey(
        'academics.Level',
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    semester = models.ForeignKey(
        'academics.Semester',
        on_delete=models.PROTECT,
        related_name='course_offerings'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'course',
                    'academic_session',
                    'programme',
                    'level',
                    'semester'
                ],
                name='unique_course_offering'
            )
        ]

    def __str__(self):
        return f"{self.course.course_code} - {self.programme.programme_name}"
