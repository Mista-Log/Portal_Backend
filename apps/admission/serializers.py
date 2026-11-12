from django.db import transaction
from rest_framework import serializers

from .models import Application, Qualification


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