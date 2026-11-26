from django.db import models




class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    ID_TYPE_CHOICES = [
        ("MATRIC", "Matriculation Number"),
        ("APPLICATION", "Application Number"),
    ]

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    id_type = models.CharField(
        max_length=20,
        choices=ID_TYPE_CHOICES
    )

    id_value = models.CharField(
        max_length=50,
        unique=True
    )

    college = models.ForeignKey(
        "academics.College",
        on_delete=models.PROTECT
    )

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT
    )

    programme = models.ForeignKey(
        "academics.Programme",
        on_delete=models.PROTECT
    )

    level = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class StudentSessionRegistration(models.Model):
    student = models.ForeignKey(
        "students.StudentProfile",
        on_delete=models.CASCADE,
        related_name="session_registrations"
    )

    session = models.ForeignKey(
        "academics.Session",
        on_delete=models.PROTECT,
        related_name="student_registrations"
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "session"],
                name="unique_student_session_registration"
            )
        ]

    def __str__(self):
        return f"{self.student.user.email} - {self.session}"