
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework import serializers

from .models import StudentProfile, StudentSessionRegistration

from apps.academics.models import (
    College,
    Department,
    Programme,
    Session,
)

User = get_user_model()


class StudentRegistrationSerializer(serializers.Serializer):

    # Personal information
    surname = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    other_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    gender = serializers.ChoiceField(
        choices=StudentProfile.GENDER_CHOICES
    )

    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(write_only=True)

    # Identification
    id_type = serializers.ChoiceField(
        choices=StudentProfile.ID_TYPE_CHOICES
    )

    id_value = serializers.CharField(max_length=50)

    # Academic information
    college = serializers.PrimaryKeyRelatedField(
        queryset=College.objects.all()
    )

    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )

    programme = serializers.PrimaryKeyRelatedField(
        queryset=Programme.objects.all()
    )

    level = serializers.CharField(max_length=20)

    session = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all()
    )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def validate_id_value(self, value):
        if StudentProfile.objects.filter(id_value=value).exists():
            raise serializers.ValidationError(
                "This identification number is already registered."
            )

        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        validated_data.pop("confirm_password")

        # Extract academic session
        session = validated_data.pop("session")

        # Extract academic profile information
        profile_data = {
            "gender": validated_data.pop("gender"),
            "id_type": validated_data.pop("id_type"),
            "id_value": validated_data.pop("id_value"),
            "college": validated_data.pop("college"),
            "department": validated_data.pop("department"),
            "programme": validated_data.pop("programme"),
            "level": validated_data.pop("level"),
        }

        # Create user account
        user = User.objects.create_user(
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("surname"),
            other_name=validated_data.pop("other_name", ""),
            phone_number=validated_data.pop("phone"),
            role="STUDENT",
        )

        # Create student profile
        student_profile = StudentProfile.objects.create(
            user=user,
            **profile_data
        )

        # Register student for academic session
        StudentSessionRegistration.objects.create(
            student=student_profile,
            session=session
        )

        return student_profile

    def to_representation(self, instance):
        return {
            "message": "Student registration successful.",
            "student": {
                "id": instance.id,
                "email": instance.user.email,
                "surname": instance.user.last_name,
                "first_name": instance.user.first_name,
                "other_name": instance.user.other_name,
                "gender": instance.gender,
                "phone": instance.user.phone_number,
                "id_type": instance.id_type,
                "id_value": instance.id_value,
                "college": instance.college_id,
                "department": instance.department_id,
                "programme": instance.programme_id,
                "level": instance.level,
                "session": instance.session_registrations.first().session_id,
            }
        }
