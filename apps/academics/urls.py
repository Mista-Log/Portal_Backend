
from django.urls import path

from .views import (
    CollegeListView,
    DepartmentListView,
    ProgrammeListView,
    SessionListView,
)


urlpatterns = [
    path("colleges/", CollegeListView.as_view(), name="college-list"),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("programmes/", ProgrammeListView.as_view(), name="programme-list"),
    path("sessions/", SessionListView.as_view(), name="session-list"),
]
