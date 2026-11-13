from rest_framework.permissions import BasePermission

from apps.account.models import UserRole


# Roles that can see and review every application.
REVIEWER_ROLES = {
    UserRole.ADMISSION_OFFICER,
    UserRole.REGISTRAR,
}

# Roles that can see applications (all of them, or only their own).
VIEWER_ROLES = REVIEWER_ROLES | {
    UserRole.PG_APPLICANT,
    UserRole.STUDENT,
}


class ApplicationPermission(BasePermission):
    """
    - Submitting (POST): PG applicants only.
    - Reviewing (PATCH): admission officers and the registrar only.
    - Viewing (GET): officers, registrar, applicants and students.
    - ICT admins and PG staff cannot access applications.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method == "POST":
            return user.role == UserRole.PG_APPLICANT

        if request.method in ("PUT", "PATCH"):
            return user.role in REVIEWER_ROLES

        return user.role in VIEWER_ROLES