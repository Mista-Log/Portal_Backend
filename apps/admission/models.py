import secrets
from django.conf import settings
from django.db import models
from django.utils import timezone


class Eligibility(models.TextChoices):
    PENDING = "pending", "Pending"
    ELIGIBLE = "eligible", "Eligible"
    NOT_ELIGIBLE = "not_eligible", "Not eligible"


class Decision(models.TextChoices):
    PENDING = "pending", "Pending"
    ADMITTED = "admitted", "Admitted"
    REJECTED = "rejected", "Rejected"


class Application(models.Model):
    application_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    # TODO: add the programme ForeignKey once the Programme model exists.

    session = models.CharField(max_length=9)  # e.g. "2025/2026"

    eligibility = models.CharField(
        max_length=20,
        choices=Eligibility.choices,
        default=Eligibility.PENDING,
    )

    decision = models.CharField(
        max_length=20,
        choices=Decision.choices,
        default=Decision.PENDING,
    )

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "session"],
                name="one_application_per_owner_per_session",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = self._generate_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_number():
        year = timezone.now().year
        while True:
            digits = "".join(secrets.choice("0123456789") for _ in range(8))
            number = f"PG-{year}-{digits}"
            if not Application.objects.filter(
                application_number=number
            ).exists():
                return number

    def __str__(self):
        return self.application_number


class Qualification(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="qualifications",
    )

    institution = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    class_of_degree = models.CharField(max_length=100)
    year_awarded = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.qualification} - {self.institution}"