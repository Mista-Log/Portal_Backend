
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import College, Department, Programme, Session
from .serializers import (
    CollegeSerializer,
    DepartmentSerializer,
    ProgrammeSerializer,
    SessionSerializer,
)


class CollegeListView(generics.ListAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [AllowAny]


class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Department.objects.select_related("college")

        college_id = self.request.query_params.get("college")

        if college_id:
            queryset = queryset.filter(college_id=college_id)

        return queryset


class ProgrammeListView(generics.ListAPIView):
    serializer_class = ProgrammeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Programme.objects.select_related("department")

        department_id = self.request.query_params.get("department")

        if department_id:
            queryset = queryset.filter(department_id=department_id)

        return queryset


class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Session.objects.filter(
            is_registration_open=True
        ).order_by("-start_date")
