
from django.db import models


class College(models.Model):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    college = models.ForeignKey(
        College,
        on_delete=models.PROTECT,
        related_name="departments"
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("college", "name")

    def __str__(self):
        return f"{self.name} - {self.college.name}"


class Programme(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="programmes"
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="Example: 2025/2026"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=False)
    is_registration_open = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
