from django.db import models

# Create your models here.



class Student(models.Model):
    user = models.OneToOneField(
        'account.User',
        on_delete=models.PROTECT,
        related_name='student_profile'
    )

    matric_number = models.CharField(
        max_length=30,
        unique=True
    )

    programme = models.ForeignKey(
        'academics.Programme',
        on_delete=models.PROTECT,
        related_name='students'
    )

    level = models.ForeignKey(
        'academics.Level',
        on_delete=models.PROTECT,
        related_name='students'
    )

    admission_year = models.PositiveSmallIntegerField()

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.matric_number
