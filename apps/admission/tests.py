from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.account.models import UserRole

from .models import Application

User = get_user_model()

PAYLOAD = {
    "session": "2025/2026",
    "date_of_birth": "1998-04-12",
    "gender": "Male",
    "nationality": "Nigerian",
    "address": "Osogbo, Osun State",
    "phone": "08012345678",
    "qualifications": [
        {
            "institution": "University of Ibadan",
            "qualification": "BSc Computer Science",
            "class_of_degree": "Second Class Upper",
            "year_awarded": 2021,
        }
    ],
}


def make_user(email, role):
    return User.objects.create_user(
        email=email,
        password="testpass123",
        first_name="Test",
        last_name="User",
        role=role,
    )


class ApplicationTests(APITestCase):
    def setUp(self):
        self.applicant = make_user(
            "applicant@test.com", UserRole.PG_APPLICANT
        )
        self.officer = make_user(
            "officer@test.com", UserRole.ADMISSION_OFFICER
        )
        self.url = "/api/applications/"

    def test_applicant_can_submit(self):
        self.client.force_authenticate(user=self.applicant)

        response = self.client.post(self.url, PAYLOAD, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["application_number"].startswith("PG-"))
        self.assertEqual(response.data["owner"], self.applicant.id)
        self.assertEqual(len(response.data["qualifications"]), 1)

    def test_cannot_apply_twice_for_same_session(self):
        self.client.force_authenticate(user=self.applicant)

        self.client.post(self.url, PAYLOAD, format="json")
        response = self.client.post(self.url, PAYLOAD, format="json")

        self.assertEqual(response.status_code, 400)

    def test_student_cannot_submit(self):
        student = make_user("student@test.com", UserRole.STUDENT)
        self.client.force_authenticate(user=student)

        response = self.client.post(self.url, PAYLOAD, format="json")

        self.assertEqual(response.status_code, 403)

    def test_applicant_only_sees_own_applications(self):
        other = make_user("other@test.com", UserRole.PG_APPLICANT)
        Application.objects.create(owner=self.applicant, session="2025/2026")
        Application.objects.create(owner=other, session="2025/2026")

        self.client.force_authenticate(user=self.applicant)
        response = self.client.get(self.url)

        data = response.data
        results = data["results"] if isinstance(data, dict) else data
        self.assertEqual(len(results), 1)

    def test_applicant_cannot_approve_themselves(self):
        application = Application.objects.create(
            owner=self.applicant, session="2025/2026"
        )

        self.client.force_authenticate(user=self.applicant)
        response = self.client.patch(
            f"{self.url}{application.id}/",
            {"decision": "admitted"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_officer_admits_and_applicant_becomes_student(self):
        application = Application.objects.create(
            owner=self.applicant, session="2025/2026"
        )

        self.client.force_authenticate(user=self.officer)
        response = self.client.patch(
            f"{self.url}{application.id}/",
            {"eligibility": "eligible", "decision": "admitted"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.applicant.refresh_from_db()
        self.assertEqual(self.applicant.role, UserRole.STUDENT)