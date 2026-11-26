from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import StudentRegistrationSerializer


class StudentRegistrationView(generics.CreateAPIView):

    serializer_class = StudentRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
