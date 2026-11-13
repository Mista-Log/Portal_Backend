from django.db import transaction
from rest_framework import serializers

from apps.account.models import UserRole

from .models import Application, Decision, Qualification


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = [
            "id",
            "institution",
            "qualification",
            "class_of_degree",
            "year_awarded",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(
        source="owner.get_full_name",
        read_only=True,
    )

    qualifications = QualificationSerializer(many=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "application_number",
            "owner",
            "owner_name",
            "session",
            "eligibility",
            "decision",
            "date_of_birth",
            "gender",
            "nationality",
            "address",
            "phone",
            "qualifications",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "application_number",
            "owner",
            "eligibility",
            "decision",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        # Only check on create, not on update.
        if self.instance is None:
            request = self.context["request"]

            already_applied = Application.objects.filter(
                owner=request.user,
                session=attrs["session"],
            ).exists()

            if already_applied:
                raise serializers.ValidationError({
                    "session": "You have already applied for this session."
                })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        qualifications_data = validated_data.pop("qualifications")

        application = Application.objects.create(**validated_data)

        for item in qualifications_data:
            Qualification.objects.create(
                application=application,
                **item,
            )

        return application


class ApplicationReviewSerializer(serializers.ModelSerializer):
    """
    Used by admission officers and the registrar to review an application.
    Only eligibility and decision can be changed.
    """

    class Meta:
        model = Application
        fields = ["eligibility", "decision"]

    @transaction.atomic
    def update(self, instance, validated_data):
        # TODO: reject the update unless the application-form payment
        # is verified (needs the Payment model).

        was_admitted = instance.decision == Decision.ADMITTED

        instance = super().update(instance, validated_data)

        # Admitted applicants become students.
        if instance.decision == Decision.ADMITTED and not was_admitted:
            owner = instance.owner

            if owner.role == UserRole.PG_APPLICANT:
                owner.role = UserRole.STUDENT
                owner.save(update_fields=["role"])

        return instance