from django.db import models

# Create your models here.

class SessionRegistration(models.Model):
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.PROTECT
    )

    academic_session = models.ForeignKey(
        'academics.AcademicSession',
        on_delete=models.PROTECT
    )

    semester = models.ForeignKey(
        'academics.Semester',
        on_delete=models.PROTECT
    )

    registration_date = models.DateField(auto_now_add=True)
    registration_status = models.CharField(max_length=30)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'academic_session', 'semester'],
                name='unique_student_session_semester'
            )
        ]

    def __str__(self):
        return str(self.student)



class CourseRegistration(models.Model):
    registration = models.ForeignKey(
        SessionRegistration,
        on_delete=models.PROTECT
    )

    course_offering = models.ForeignKey(
        'courses.CourseOffering',
        on_delete=models.PROTECT
    )

    registration_date = models.DateField(auto_now_add=True)
    registration_status = models.CharField(max_length=30)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['registration', 'course_offering'],
                name='unique_course_per_registration'
            )
        ]

    def __str__(self):
        return str(self.course_offering)